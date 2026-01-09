from utils import my_utils

# my_utils.save_coordinates(my_utils.normalize_tree_coords(my_utils.read_in_coords("normalized_tree_d_coords.txt")), "normalized_bottom_tree_d_coords.txt")

coords = my_utils.read_in_coords("normalized_bottom_tree_d_coords.txt")

mm_converted = my_utils.inches_to_mm_rounded(coords)

my_utils.save_coordinates(mm_converted, "bottom_normalized_tree_d_coords_mm.txt")