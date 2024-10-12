import os
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
import logging

from utils import load_config, clean_and_convert, fill_na_values

# Load configuration
config = load_config()
PN_REPORT_FILE = config['paths']['pn_report']
PN_REPORT_FILE_CLUSTERED = config['paths']['processed']['pn_report_clustered']
PROCESSED_PATH = config['paths']['processed']['path']

# Set up basic logging configuration
logging.basicConfig(level=logging.DEBUG,  # Set the logging level
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Define the format
logger = logging.getLogger(__name__)

def generate_clusters(data_path=PN_REPORT_FILE, min_clusters=5, max_clusters=10, random_seed=56):
    data = clean_and_convert(pd.read_csv(data_path))
    data = fill_na_values(data)

    cols_not_to_use = ["Player", "Hands", "WWSF", "BB Won", "Avg PF All-In Equity"]
    df_to_cluster = data.drop(columns=cols_not_to_use)

    # Scale the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_to_cluster)

    # Find the optimal number of clusters using silhouette score
    best_score = -1
    best_k = 0
    best_model = None

    for k in range(min_clusters, max_clusters):
        kmeans = KMeans(n_clusters=k, random_state=random_seed)
        kmeans.fit(scaled_data)
        score = silhouette_score(scaled_data, kmeans.labels_)
        logger.debug(f"Silhouette score: {score:.4f} for {k} clusters")
        if score > best_score:
            best_score = score
            best_k = k
            best_model = kmeans

    # Display the optimal number of clusters
    logger.info(f"Optimal number of clusters: {best_k} with silhouette score: {best_score:.4f}")

    # Save the cluster labels back to the original dataframe for further analysis
    data['BB Won/100'] = (data['BB Won'] / data['Hands'].replace(0, np.nan)) * 100
    data['Cluster'] = best_model.labels_
    data.to_csv(PN_REPORT_FILE_CLUSTERED, index=False)  # Set index=False to avoid writing row indices

def interpret_clusters(data_path=PN_REPORT_FILE_CLUSTERED):
    data = pd.read_csv(data_path)
    num_clusters = len(data['Cluster'].unique())

    # Calculate the average stats for each cluster
    overall_average = data.drop(columns='Player').mean().round(2)
    average_stats = data.drop(columns='Player').groupby('Cluster').mean().round(2)
    diff_from_overall = (average_stats - overall_average).round(2)

    # Save to csv files
    average_stats.to_csv(os.path.join(PROCESSED_PATH, "cluster_average_stats.csv"), index=True)
    diff_from_overall.to_csv(os.path.join(PROCESSED_PATH, "cluster_diff_from_overall_average.csv"), index=True)
    overall_average_df = overall_average.to_frame(name='Overall Average').T  # Convert Series to DataFrame
    overall_average_df.to_csv(os.path.join(PROCESSED_PATH, "overall_average_stats.csv"), index=False)

    # Rank clusters by average BB Won/100
    average_bb_won_per_100 = average_stats['BB Won/100']
    ranked_clusters = average_bb_won_per_100.sort_values(ascending=False)

    # Count the number of players in each cluster
    players_per_cluster = data['Cluster'].value_counts().sort_index()

    # Save average stats and differences to a text file
    with open(PROCESSED_PATH + "average_stats_per_cluster.txt", "w") as f:
        f.write("Average stats for each cluster:\n")
        for cluster in ranked_clusters.index:
            f.write(f"\nCluster {cluster}")
            f.write(f"\nNumber of Players: {players_per_cluster[cluster]}")
            f.write(f"\nAverage Stats:\n")
            cluster_avg_stats = average_stats.loc[cluster]
            for stat, value in cluster_avg_stats.items():
                diff_value = diff_from_overall.loc[cluster, stat]
                f.write(f"{stat}: {value} (Diff from Overall: {diff_value})\n")

    logger.info("Average stats and differences written to text file.")

    # log ranked clusters and number of players per cluster
    logger.info("\nClusters ranked by average BB Won/100:")
    logger.info(f"{ranked_clusters}")

    # Create a dictionary of clusters
    cluster_dict = {}
    for cluster in range(num_clusters):
        cluster_dict[cluster] = data[data['Cluster'] == cluster]

    # Save players in each cluster to a JSON file
    players_json = {f'Cluster_{cluster}': ','.join([f"'{p}'".lower() for p in set(cluster_dict[cluster]['Player'])]) for
                    cluster in range(num_clusters)}
    with open(os.path.join(PROCESSED_PATH, 'players_per_cluster.json'), 'w') as json_file:
        json.dump(players_json, json_file, indent=4)


def calculate_feature_importance(data_path=PN_REPORT_FILE_CLUSTERED):
    data = pd.read_csv(data_path)
    # Determine feature importance
    anova_results = {}
    df_numeric = data.drop(columns='Player')
    for col in df_numeric.columns:
        # Perform ANOVA to check if means of the feature differ across clusters
        f_val, p_val = stats.f_oneway(
            *[df_numeric[col][data['Cluster'] == cluster] for cluster in data['Cluster'].unique()])
        anova_results[col] = f_val
    # Convert to DataFrame for easier sorting
    anova_df = pd.DataFrame(list(anova_results.items()), columns=['Stat', 'F-Value'])
    # Sort by F-Value (importance)
    anova_df = anova_df.sort_values(by='F-Value', ascending=False)
    anova_df.to_csv(PROCESSED_PATH + "anova_feature_importance.csv", index=False)

    # Create a random forest classifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    # Fit the model using the stats to predict cluster labels
    rf.fit(df_numeric, data['Cluster'])
    # Get feature importances from the trained model
    feature_importances = rf.feature_importances_
    # Convert to DataFrame for easier sorting
    importance_df = pd.DataFrame({
        'Stat': df_numeric.columns,
        'Importance': feature_importances
    })
    # Sort by feature importance
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    importance_df.to_csv(PROCESSED_PATH + "random_forest_feature_importance.csv", index=False)

if __name__ == '__main__':
    generate_clusters()
    interpret_clusters()
    calculate_feature_importance()
