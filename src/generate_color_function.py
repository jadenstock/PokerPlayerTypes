import pandas as pd
import os
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from utils import load_config
config = load_config()
PN_REPORT_FILE_CLUSTERED = config['paths']['pn_report_clustered']

def generate_function_string():
    # Load the clustered players data
    file_path = "clustered_pn_players_data/clustered_players_report_10_9_24.csv"
    data = pd.read_csv(file_path)

    # Replace '-' with NaN and clean string columns
    data = data.replace('-', np.nan)

    # Convert relevant columns to numeric, handling commas and other issues
    cols_to_convert = ["PFR/VPIP", "VPIP", "PFR", "Limp", "CC 2Bet PF", "Total AFq", "3Bet PF",
                       "4Bet PF", "CBet F", "Fold to F CBet", "XR Flop", "WWSF",
                       "2Bet PF & Fold", "Fold to Steal", "Att To Steal"]
    for col in cols_to_convert:
        if col in data.columns:
            data[col] = data[col].astype(str).str.replace(',', '').str.replace(' ', '').replace('', np.nan).astype(
                float)

    # Drop any rows with NaN values
    data = data.dropna()

    # Fit a decision tree to predict the cluster based on the stats
    X = data[cols_to_convert]
    y = data['Cluster']
    tree = DecisionTreeClassifier(random_state=42)
    tree.fit(X, y)

    # Generate the tree rules for function string
    def recurse(node):
        if tree.tree_.children_left[node] == tree.tree_.children_right[node]:  # Leaf node
            return f"rgb({colors[int(tree.tree_.value[node].argmax())]})"

        feature = cols_to_convert[tree.tree_.feature[node]]
        threshold = tree.tree_.threshold[node]
        left_child = tree.tree_.children_left[node]
        right_child = tree.tree_.children_right[node]

        # Build the condition
        condition = f"({feature} <= {threshold})"

        # Recursive calls for left and right
        left = recurse(left_child)
        right = recurse(right_child)

        return f"if({condition},{left},{right})"

    # Start recursion from the root node
    function_str = recurse(0)

    # Replace variable names with the desired format
    for col in cols_to_convert:
        function_str = function_str.replace(col, f'#{col}#')

    # Remove excess whitespace outside of variable names
    clean_str = ""
    in_var_name = False
    for char in function_str:
        if char == '#':
            in_var_name = not in_var_name
            clean_str += char
        elif not in_var_name and char.isspace():
            continue
        else:
            clean_str += char

    var_map = {
        "##PFR#/#VPIP##": '#PFR/VPIP#',
        "Limp": "Preflop Limp",
        "3Bet PF": "3Bet Preflop",
        "4Bet PF": "4Bet Preflop",
        "CBet F": "CBet Flop",
        "XR Flop": "Check Raise Flop",
        "CC 2Bet PF": "Cold Call 2Bet PF",
        "2Bet PF & Fold": "Fold to PF 3Bet After Raise",
        "Fold to Steal": "Fold to LP Steal",
    }
    for k, v in var_map.items():
        clean_str = clean_str.replace(k, v)

    with open('clustered_pn_players_data/function_representation.txt', 'w') as f:
        f.write(clean_str)

    return clean_str


if __name__ == '__main__':
    colors = {
        0: "255,100,100",  # second most red
        1: "255,0,0",  # most red
        2: "200,255,100",  # muted green with a hint of yellow
        3: "100,255,100",  # light green
        4: "0,200,0"  # most green
    }

    colors = {
        5: "139,0,0",
        0: "255,0,0",
        4: "255,165,000",
        2: "255,255,0",
        1: "144,238,144",
        3: "0,200,0"
    }

    result = generate_function_string()
    print(result)