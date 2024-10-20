import numpy as np
import pandas as pd
import logging
from decision_tree import create_decision_tree, run_decision_tree

from utils import load_config

config = load_config()
PN_REPORT_FILE_CLUSTERED = config['paths']['processed']['pn_report_clustered']

# Set up basic logging configuration
logging.basicConfig(level=logging.DEBUG,  # Set the logging level
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Define the format
logger = logging.getLogger(__name__)

# Perturbation function to add noise to a stat
def perturb_stat(stat_value, noise_level=0.1):
    """
    Apply noise to a stat value. Noise is a random percentage change.
    """
    noise = np.random.normal(loc=0, scale=noise_level)
    return stat_value * (1 + noise)


# Function to analyze feature importance and cluster robustness for a single player
def analyze_player_importance(player_name, tree, data, cols_to_convert, noise_level=0.1, num_perturbations=100):
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
    """
    # Locate the row for the specified player
    player_row = data[data['Player'] == player_name].iloc[0][cols_to_convert].values

    # Predict the initial cluster
    initial_cluster = run_decision_tree(tree, player_row)

    # Dictionary to store how often each stat causes a cluster change
    importance_dict = {col: 0 for col in cols_to_convert}

    # Count the number of times the cluster stays the same (robustness measure)
    same_cluster_count = 0

    # Loop through each stat and perturb it
    for _ in range(num_perturbations):
        for stat_index, stat_name in enumerate(cols_to_convert):
            # Copy the player's original row
            perturbed_row = player_row.copy()

            # Apply noise to the specific stat
            perturbed_row[stat_index] = perturb_stat(perturbed_row[stat_index], noise_level=noise_level)

            # Predict the cluster with the perturbed stat
            perturbed_cluster = run_decision_tree(tree, perturbed_row)

            # Check if the cluster has changed
            if perturbed_cluster != initial_cluster:
                importance_dict[stat_name] += 1
            else:
                same_cluster_count += 1

    # Calculate robustness (percentage of times the cluster remained the same)
    robustness = same_cluster_count / (len(cols_to_convert) * num_perturbations)

    return importance_dict, robustness

def run_feature_importance_for_player(player_name):
    # Load the decision tree and data
    tree, cols_to_convert = create_decision_tree()
    data = pd.read_csv(PN_REPORT_FILE_CLUSTERED)

    # Run the analysis for a given player
    importance_dict, robustness = analyze_player_importance(player_name, tree, data, cols_to_convert, noise_level=0.3)

    logger.info(f"Feature Importance for {player_name}:")
    for stat, count in importance_dict.items():
        logger.info(f"{stat}: {count} cluster changes")

    logger.info(f"Robustness: {robustness * 100:.2f}% of the time, the cluster stayed the same")


if __name__ == '__main__':
    run_feature_importance_for_player("alexr")
