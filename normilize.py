from utils import my_utils

coords = my_utils.read_in_coords("tree_d_coords.txt")

normilized_coords = my_utils.normalize_tree_coords(coords)

my_utils.save_coordinates(normilized_coords, "normalized_tree_d_coords.txt")