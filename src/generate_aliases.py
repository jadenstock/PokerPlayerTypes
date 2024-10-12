import pandas as pd
from rapidfuzz import process, fuzz
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import euclidean
import logging

from utils import load_config, clean_and_convert, fill_na_values

config = load_config()
PN_REPORT = config['paths']['pn_report']

# Set up basic logging configuration
logging.basicConfig(level=logging.DEBUG,  # Set the logging level
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Define the format
logger = logging.getLogger(__name__)

def generate_alises(file_path = PN_REPORT):
    # Load and clean the data
    data = pd.read_csv(file_path)
    data = clean_and_convert(data)
    data = fill_na_values(data)

    # Extract player names and stats
    player_names = data['Player'].unique()

    # Standardize the stats for better comparison
    scaler = StandardScaler()
    columns_to_cluster_on = ['PFR','VPIP'] # '3Bet PF', '4Bet PF'
    scaled_stats = scaler.fit_transform(data[columns_to_cluster_on])

    # Function to calculate stat similarity using Euclidean distance
    def stat_similarity_by_player(player1_idx, player2_idx, scaled_stats):
        return 1 / (1 + euclidean(scaled_stats[player1_idx], scaled_stats[player2_idx]))

    # Define a function to find similar names and similar stats
    def find_similar_names_and_stats(names, stats, threshold=60, stat_weight=0.5):
        similar_name_sets = []
        used_names = set()

        # Iterate over each name to find similar names and stats
        for idx, name in enumerate(names):
            if name not in used_names:
                # Find similar names based on string similarity
                matches = process.extract(name, names, scorer=fuzz.ratio, score_cutoff=threshold)
                if len(matches) > 1:
                    logger.debug(f"similar names to {name} are {matches}")

                similar_names = []
                for match in matches:
                    match_name = match[0]
                    match_idx = list(names).index(match_name)

                    # Calculate stat similarity
                    stat_sim = stat_similarity_by_player(idx, match_idx, stats)
                    if name!= match_name:
                        logger.debug(f"stat similarity between {name} and {match_name} is {stat_sim}")

                    # Combine name similarity and stat similarity (weighted average)
                    combined_score = (match[1] / 100) * (1 - stat_weight) + stat_sim * stat_weight

                    # If the combined score is high, treat them as aliases
                    if combined_score > threshold:  # Adjust the threshold as needed
                        similar_names.append(match_name)

                if len(similar_names) > 1:
                    similar_name_sets.append(similar_names)

                # Mark the names as used
                used_names.update(similar_names)

        return similar_name_sets

    # Find sets of similar player names and stats (adjust threshold and stat weight as needed)
    alias_sets = find_similar_names_and_stats(player_names, scaled_stats, threshold=85, stat_weight=0.5)

    # Print the sets of aliases
    for alias_set in alias_sets:
        print(f"Possible aliases: {alias_set}")


if __name__ == "__main__":
    generate_alises()