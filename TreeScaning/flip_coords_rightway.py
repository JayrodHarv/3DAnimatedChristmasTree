import my_utils

def flip_rightway():
    coords = my_utils.read_in_coords("tree_d_coords.txt")
    for coord in coords:
        coord[1], coord[2] = coord[2], coord[1]
    
    # write to file
    result = ""
    for coord in coords:
        result += f"{coord}\n"
    with open("tree_d_coords.txt", "w") as file:
        file.write(f"{result}")
        
flip_rightway()