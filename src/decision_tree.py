import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from utils import load_config

config = load_config()
PN_REPORT_FILE_CLUSTERED = config['paths']['processed']['pn_report_clustered']

# Convert relevant columns to numeric, handling commas and other issues
COLS_TO_CONVERT = ["PFR/VPIP", "VPIP", "PFR", "Limp", "CC 2Bet PF", "Total AFq", "3Bet PF",
                   "4Bet PF", "CBet F", "Fold to F CBet", "XR Flop", "WWSF",
                   "2Bet PF & Fold", "Fold to Steal", "Att To Steal"]

# Function to create and return the decision tree model
def create_decision_tree(data_path=PN_REPORT_FILE_CLUSTERED):
    # Load the clustered players data
    data = pd.read_csv(data_path)

    # Define input features and target
    X = data[COLS_TO_CONVERT]
    y = data['Cluster']

    # Create and fit the decision tree
    tree = DecisionTreeClassifier(random_state=42)
    tree.fit(X, y)

    return tree, COLS_TO_CONVERT


# Function to predict the cluster for a given row using the trained decision tree
def run_decision_tree(tree, input_row, cols=COLS_TO_CONVERT):
    if cols != None:
        row_df = pd.DataFrame([input_row], columns=cols)
        return tree.predict(row_df)[0]
    else:
        # works but will give warnings
        return tree.predict([input_row])