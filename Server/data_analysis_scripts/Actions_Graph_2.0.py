import networkx as nx
import matplotlib.pyplot as plt
import json
import os
import argparse


def json_get_game_actions(task, actions, percentage, filepath):
    steps = []
    last_step = ''
    with open(filepath, 'r') as f:
        json_content = json.load(f)
        for item in json_content['steps']:
            if item[1] in actions.keys() and item[0] in actions[item[1]]:
                if len(steps) == 0 and last_step == '':
                    last_step = item[1]
                elif last_step != '' and last_step != item[1]:
                    steps.append((last_step, item[1]))
                    last_step = item[1]
    return steps


def normalize_counts(edge_counts):
    max_count = max(edge_counts.values())
    min_count = min(edge_counts.values())

    if max_count == min_count:
        return {k: 1 for k in edge_counts}

    normalized_counts = {}
    for k, v in edge_counts.items():
        # Normalize counts to be between 1 and 10
        normalized_counts[k] = 1 + 9 * (v - min_count) / (max_count - min_count)
    return normalized_counts


def create_actions_graph(task, actions_dict, percentage, count_multiple, save_path):
    #base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    #directory = os.path.join(base_directory, str(percentage))
    directory = os.path.join("Parsed_Data", str(percentage))
    # base_directory = r'C:\Users\user\Desktop\final_project\Minecraft-Data-Analysis-Project\Server\Parsed_Data\10'
    # directory = base_directory#os.path.join(base_directory, str(percentage))
    count = 1
    sequences = {}

    actions = {}
    for d in actions_dict:
        actions[d['name'].replace('_', ' ')] = d['actions']

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        actions_per_player = json_get_game_actions(task, actions, percentage, filepath)
        sequences[f'Player {count}'] = actions_per_player
        count += 1

    G = nx.DiGraph()

    # Add nodes for each action
    for action in actions:
        G.add_node(action)

    # Create a dictionary to count edges
    edge_counts = {}

    for player in sequences:
        if count_multiple:
            transitions = sequences[player]
        else:
            transitions = set(sequences[player])
        for action_pair in transitions:
            if action_pair in edge_counts:
                edge_counts[action_pair] += 1
            else:
                edge_counts[action_pair] = 1

    # Normalize edge counts for width
    if len(edge_counts.keys())>0:
        normalized_counts = normalize_counts(edge_counts)
    else:
        normalized_counts = edge_counts

    # Draw the graph using a different layout algorithm
    pos = nx.spring_layout(G, k=0.3)  # Increase the spacing
    plt.figure(figsize=(15, 10))  # Increase figure size
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=5000, font_size=14,
            font_weight='bold')  # Larger node and font size

    # Draw directed edges with normalized widths and larger arrowheads
    for (source, target), width in normalized_counts.items():
        nx.draw_networkx_edges(
            G, pos, edgelist=[(source, target)], width=width, alpha=0.7, edge_color='black',
            arrowstyle='-|>', arrowsize=20, connectionstyle='arc3,rad=0.2'
        )

    plt.title("Actions and Players", fontsize=20)

    # Save the plot as a JPEG file
    plt.savefig(save_path, format='jpeg')

    # plt.show()

# ['white tulip', 'dark oak log', 'stone axe', 'stone', 'fly one cm']
# [{'name':'stone', 'actions':['mines']},{"name":"dark_oak_log","actions":["mines"]},{"name":"crafting_table","actions":["pick-ups"]}]
# Example usage with the flag set to True or False and saving the plot
# save_path = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\actions_graph.jpeg'
# create_actions_graph('shira', [
#     {'name': 'white tulip', 'actions': ['uses', 'pick-ups']},
#     {'name': 'dark oak log', 'actions': ['crafts', 'uses', 'pick-ups']},
#     {'name': 'stone axe', 'actions': ['uses', 'pick-ups', 'crafts']},
#     {'name': 'stone', 'actions': ['mines', 'uses']},
#     {'name': 'fly one cm', 'actions': ['physical']}
# ], 100, count_multiple=False, save_path=save_path)


def main():
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--task', type=str, default='House Building from Scratch Task', help='name of a task')
    parser.add_argument('--percentage', type=int, default=10, help='Percentage of data to process')
    parser.add_argument('--actions', type=str, required=True, help='JSON string of actions')

    args = parser.parse_args()
    task = args.task
    percentage = args.percentage
    # try:
    #     actions = json.loads(args.actions)
    # except json.JSONDecodeError as e:
    #     print(f"Error parsing actions: {e}")
    #     return

    try:
        actions = json.loads("[{\"name\":\"oak log\",\"actions\":[\"mines\"]}]")
    except json.JSONDecodeError as e:
        print(f"Error parsing actions: {e}")
        return


    # save_filename = 'actions_graph.jpeg'
    # save_path = os.path.join(base_directory, save_filename)

    save_filename = r'C:\Users\user\Desktop\final_project\Minecraft-Data-Analysis-Project\server\actions_graph.jpeg'    
    
    create_actions_graph(task, actions, percentage, count_multiple=False, save_path=save_filename)

    # print( json.dumps({
    #     'action_graph_path': save_filename
    # }) )


if __name__ == "__main__":
    main()