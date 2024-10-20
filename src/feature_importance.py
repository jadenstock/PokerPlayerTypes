import numpy as np
import pandas as pd
import logging
from decision_tree import create_decision_tree, run_decision_tree

from utils import load_config

config = load_config()
PN_REPORT_FILE_CLUSTERED = config['paths']['processed']['pn_report_clustered']

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def perturb_stat(stat_value, noise_level=0.1, min_value=0, max_value=100):
    """
    Apply noise to a stat value, ensuring it stays within bounds.
    Noise is a random percentage change.
    """
    noise = np.random.normal(loc=0, scale=noise_level)
    perturbed_value = stat_value * (1 + noise)
    return np.clip(perturbed_value, min_value, max_value)


def perturb_vpip_pfr(vpip_value, pfr_value, noise_level=0.1):
    """
    Apply noise to both VPIP and PFR, ensuring that PFR <= VPIP after perturbation.
    """
    perturbed_vpip = perturb_stat(vpip_value, noise_level=noise_level)
    perturbed_pfr = min(perturb_stat(pfr_value, noise_level=noise_level), perturbed_vpip)
    perturbed_prf_over_pip = perturbed_pfr / perturbed_vpip
    return perturbed_vpip, perturbed_pfr, perturbed_prf_over_pip


# Updated function to handle recalculation of derived stats
def analyze_player_importance(player_name, tree, data, cols_to_convert, noise_level=0.1, num_perturbations=1000):
    """
    Analyze the importance of each stat for a player by perturbing each stat and
    observing how the player's predicted cluster changes.

    Args:
    - player_name: Name of the player (row) to analyze.
    - tree: Trained decision tree model.
    - data: Full dataframe of player stats.
    - cols_to_convert: List of stat column names.
    - noise_level: How much noise to apply to each stat (default 10%).
    - num_perturbations: How many times to perturb each stat and run the classifier.

    Returns:
    - importance_dict: Dictionary of how many times each stat caused a cluster change.
    - robustness: Percentage of times the cluster stayed the same across all perturbations.
    - cluster_distribution: A dictionary with the count of each cluster.
    """
    # Locate the row for the specified player
    player_row = data[data['Player'] == player_name].iloc[0][cols_to_convert].values
    initial_cluster = run_decision_tree(tree, player_row) # Predict the initial cluster
    importance_dict = {col: 0 for col in cols_to_convert} # Dictionary to store how often each stat causes a cluster change
    cluster_distribution = {} # Track the number of occurrences for each cluster
    same_cluster_count = 0 # Count the number of times the cluster stays the same (robustness measure)

    # Loop through each stat and perturb it
    for _ in range(num_perturbations):
        perturbed_row = player_row.copy()

        for stat_index, stat_name in enumerate(cols_to_convert):
            # Handle VPIP/PFR together and recalculate VPIP/PFR after perturbation
            if stat_name == 'PFR/VPIP':
                vpip_index = cols_to_convert.index('VPIP')
                pfr_index = cols_to_convert.index('PFR')
                pfr_to_vpip_index = cols_to_convert.index('PFR/VPIP')

                # Perturb both VPIP and PFR
                perturbed_vpip, perturbed_pfr, perturbed_pfr_to_vpip = perturb_vpip_pfr(player_row[vpip_index], player_row[pfr_index],
                                                                 noise_level=noise_level)

                # Update perturbed row with new VPIP and PFR values
                perturbed_row[vpip_index] = perturbed_vpip
                perturbed_row[pfr_index] = perturbed_pfr
                perturbed_row[pfr_to_vpip_index] = perturbed_pfr_to_vpip
            elif stat_name in ['PFR', 'VPIP', 'WWSF', 'Total AFq', 'Att To Steal']:
                continue
            else:
                # Perturb individual stat
                perturbed_row[stat_index] = perturb_stat(perturbed_row[stat_index], noise_level=noise_level)

        # Predict the cluster with the perturbed row
        perturbed_cluster = run_decision_tree(tree, perturbed_row)

        # Log which cluster comes up
        if perturbed_cluster in cluster_distribution:
            cluster_distribution[perturbed_cluster] += 1
        else:
            cluster_distribution[perturbed_cluster] = 1

        # Check if the cluster has changed
        if perturbed_cluster != initial_cluster:
            importance_dict[stat_name] += 1
        else:
            same_cluster_count += 1

    # Calculate robustness (percentage of times the cluster remained the same)
    robustness = same_cluster_count / (len(cols_to_convert) * num_perturbations)

    return importance_dict, robustness, cluster_distribution


def run_feature_importance_for_player(player_name):
    # Load the decision tree and data
    tree, cols_to_convert = create_decision_tree()
    data = pd.read_csv(PN_REPORT_FILE_CLUSTERED)

    # Run the analysis for a given player
    importance_dict, robustness, cluster_distribution = analyze_player_importance(
        player_name, tree, data, cols_to_convert, noise_level=0.1)

    logger.info(f"Feature Importance for {player_name}:")

    logger.info(f"Robustness: {robustness * 100:.2f}% of the time, the cluster stayed the same")

    # Log the cluster distribution
    total_perturbations = sum(cluster_distribution.values())
    logger.info(f"Cluster distribution after perturbations:")
    for cluster, count in cluster_distribution.items():
        percentage = (count / total_perturbations) * 100
        logger.info(f"Cluster {cluster}: {percentage:.2f}%")

    logger.info(f"Stat Level importance:")
    for stat, count in importance_dict.items():
        logger.info(f"{stat}: {count} cluster changes")


if __name__ == '__main__':
    run_feature_importance_for_player("alexr")
