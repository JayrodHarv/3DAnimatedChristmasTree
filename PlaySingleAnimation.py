import argparse
from utils import runtime

from animations import ANIMATIONS

DEFAULT_COORDS_FILE = "bottom_normalized_tree_d_coords_mm.txt" # set coords file as this by default

def parse_args():
    parser = argparse.ArgumentParser(
        description="3D Christmas Tree Animation Scheduler"
    )

    parser.add_argument(
        "--coords",
        nargs="?",
        default=DEFAULT_COORDS_FILE,
        help="Path to coordinate file"
    )

    return parser.parse_args()

args = parse_args()

# ===================================================
# LED SETUP
# ===================================================
coords, pixels = runtime.setup_tree(
    coords_file=args.coords
)

print("Tree animation scheduler running...")

try:
    while True:
        print("Christmas Tree Animations:")
        i = 1
        for anim in ANIMATIONS:
            print("\t" + str(i) + ") " + anim.name)
            i += 1

        try:
            number = int(input("Please select an animation to play by entering a number..."))

            if number - 1 < 0 or number - 1 > len(ANIMATIONS):
                raise ValueError
            
            AnimClass = ANIMATIONS[number - 1]

            anim = AnimClass(coords, pixels)

            print(f"Playing {anim.name}")

            anim.run(duration=None, fps=30)

            # small blackout between animations
            pixels.fill((0,0,0))
            pixels.show()

        except ValueError:
            print("You must enter a valid number. Please try again.")

except KeyboardInterrupt:
    pixels.fill((0,0,0))
    pixels.show()
    print("\nStopped.")