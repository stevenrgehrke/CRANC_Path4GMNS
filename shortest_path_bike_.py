# import yaml

# # Load the settings.yml to check if the modes are being loaded
# with open('data/settings.yml', 'r') as file:
#     settings = yaml.safe_load(file)
#     print("Loaded agents:", settings['agents'])  # Print all the agent modes





import path4gmns as pg

# Load the network data
network = pg.read_network(input_dir='data/Chicago_Sketch')

# Retrieve the shortest path using the type 'w' for walking mode
print('\nShortest path (node id) from node 1 to node 2, '
      + network.find_shortest_path(1, 10, mode='b'))  # Using type 'w'

# Retrieve the shortest path (link sequence) using the type 'w' for walking mode
print('\nShortest path (link id) from node 1 to node 2, '
      + network.find_shortest_path(1, 10, mode='b', seq_type='link'))  # Using type 'w'