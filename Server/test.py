import requests
import matplotlib.pyplot as plt
import pandas as pd
# url = 'https://minecraft-analysis-422617.oa.r.appspot.com/download'
# params = {
#     'videoPath': 'data/10.0/cheeky-cornflower-setter-02e496ce4abb-20220421-093149.mp4'
# }

# response = requests.get(url, params=params)

# if response.status_code == 200:
#     with open('download.zip', 'wb') as f:
#         f.write(response.content)
#     print('Download successful.')
# else:
#     print('Error:', response.status_code)



def test_get_video_paths(base_url, json_file_name):
    # Construct the full URL for the endpoint
    url = f"{base_url}/get-video-paths"
    
    # Define the query parameters
    params = {
        'jsonFile': json_file_name
    }
    
    try:
        # Send the GET request to the endpoint
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse and print the JSON response
            video_paths = response.json()
            print(f"Video paths in {json_file_name}:")
            for path in video_paths:
                print(path)
        else:
            print(f"Failed to get video paths. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")



def test_analyze_endpoint(base_url, percentage=100, items=None):
    # Construct the full URL for the endpoint
    url = f"{base_url}/TimeSeriesStates"
    
    # Define the query parameters
    params = {
        'percentage': percentage,
        'items': items or 'mines.stone,mines.cobblestone,pick-ups.cobblestone,uses.stone pickaxe'
    }
    
    try:
        # Send the GET request to the endpoint
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            print(f"Analysis results for {percentage}% of data with items {params['items']}:")
            for entry in data:
                print(entry)

            # Plot the graph
            plot_graph(data, params['items'].split(','))
        else:
            print(f"Failed to analyze data. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def plot_graph(data, items):
    """
    Plot the graph based on the analysis results.

    :param data: The analysis results as a list of dictionaries.
    :param items: The list of items to plot.
    """
    times = [entry['time'] for entry in data]
    
    plt.figure(figsize=(12, 8))
    
    for item in items:
        quantities = [entry[item] for entry in data]
        plt.plot(times, quantities, label=item, marker='o', linestyle='-')
    
    plt.xlabel('Time (seconds)')
    plt.ylabel('Frequency')
    plt.title('Action Frequencies Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    # Base URL of your server
    base_url = 'https://minecraft-analysis-422617.oa.r.appspot.com'
    base_url = 'http://localhost:8080'
    # Name of the JSON file to query
    json_file_name = 'House_Building.json'
    
    # Test the endpoint
    # test_get_video_paths(base_url, json_file_name)


    percentage = 100
    
    # Comma-separated list of items to include in the analysis
    items = 'mines.stone,mines.cobblestone,pick-ups.cobblestone,uses.stone pickaxe'
    
    # Test the endpoint
    test_analyze_endpoint(base_url, percentage, items)
