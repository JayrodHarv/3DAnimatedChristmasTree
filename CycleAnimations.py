import random
from utils import my_utils
from utils import runtime
import argparse

from animations import ANIMATIONS

DEFAULT_ORDER = "shuffle" # Random order by default

DEFAULT_DURATION = "60" # 1 minute duration by default

DEFAULT_COORDS_FILE = "tree_d_coords.txt" # set coords file as this by default

def parse_args():
    parser = argparse.ArgumentParser(
        description="3D Christmas Tree Animation Scheduler"
    )

    parser.add_argument(
        "--order",
        choices=["in-order", "shuffle"],
        default=DEFAULT_ORDER,
        help="Animation play order"
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=DEFAULT_DURATION,
        help="Duration that each animation plays for in seconds"
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Speed multiplier for animations"
    )

    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frames per second for animations"
    )

    parser.add_argument(
        "--coords",
        nargs="?",
        default=DEFAULT_COORDS_FILE,
        help="Path to coordinate file"
    )

    return parser.parse_args()

args = parse_args()

animations = ANIMATIONS[:]  # copy list

# ===================================================
# LED SETUP
# ===================================================
coords, pixels = runtime.setup_tree(
    coords_file=args.coords
)

# ===================================================
# SCHEDULER LOOP
# ===================================================

print("Tree animation scheduler running. Press ctrl+c to stop...")

try:
    while True:
        if args.order == "shuffle":
            random.shuffle(animations)

        for AnimClass in animations:
            anim = AnimClass(coords, pixels)
            # print(f"Playing {anim.name} for {args.duration} seconds")
            anim.run(duration=args.duration, fps=args.fps, speed=args.speed)
            pixels.fill((0,0,0))

except KeyboardInterrupt:
    pixels.fill((0,0,0))
    pixels.show()
    print("\nStopped.")