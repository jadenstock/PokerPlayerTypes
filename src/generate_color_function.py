from utils import load_config

from decision_tree import create_decision_tree

config = load_config()
PN_REPORT_FILE_CLUSTERED = config['paths']['processed']['pn_report_clustered']
COLOR_CLASSIFICATION_FUNCTION_FILE = config['paths']['processed']['color_function_file']


# Function to generate the string representation of the decision tree
def generate_function_string(tree, cols_to_convert, colors, output_path=COLOR_CLASSIFICATION_FUNCTION_FILE):
    # Helper function for recursion
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

    # Perform variable name replacements (optional)
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

    # Save the function string to a file
    with open(output_path, 'w') as f:
        f.write(clean_str)

    return clean_str


if __name__ == '__main__':
    # Example color map
    colors = {
        0: "153,50,204",  # Lighter purple
        1: "165,42,42",  # Slightly lighter dark red
        2: "0,128,0",  # Most green
        3: "255,102,102",  # Lighter shade of red
        4: "144,238,144",  # Lighter green
        5: "255,255,0"  # Yellow
    }

    # Create the decision tree
    tree, cols_to_convert = create_decision_tree()

    # Generate the function string
    function_str = generate_function_string(tree, cols_to_convert, colors)
    print(function_str)

    # Example usage of running the decision tree on an input row
    # Assuming `input_row` is a list or array-like structure with values for each feature
    # result = run_decision_tree(tree, input_row)
    # print(f"Predicted cluster: {result}")
