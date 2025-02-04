# import path4gmns.io
# help(path4gmns.io.read_network)

# # Assuming you need to read the network data first
# node_file = './data/Arizona/node.csv'
# link_file = './data/Arizona/link.csv'

# network = path4gmns.io.read_network(
#     "./data/Arizona/node.csv",
#     "./data/Arizona/link.csv",
#     length_unit="m"  # Ensure this is passed as a keyword argument
# )


# Now you can use the 'network' object for pathfinding if such functionality exists

import path4gmns as pg

# Specify the directory containing the network dataset
network = pg.read_network(input_dir='gmns_network')

# Find the shortest path (node sequence) from node 1 to node 2
print('\nShortest path (node id) from node 1 to node 2: ',
      network.find_shortest_path(1, 2))

# Find the shortest path (link sequence) from node 1 to node 2
print('\nShortest path (link id) from node 1 to node 2: ',
      network.find_shortest_path(1, 2, seq_type='link'))
