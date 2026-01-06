from .breathing_tree import run as breathing_tree
from .enchantment_glint import run as enchantment_glint
from .fire import run as fire
from .intersecting_planes import run as intersecting_planes
from .rainbow_swirl import run as rainbow_swirl
from .random_direction_scan import run as random_direction_scan
from .random_rgb_all import run as random_rgb_all
from .rgb_spheres import run as rgb_spheres
from .scrolling_text import run as scrolling_text
from .smooth_rgb_spectrum import run as smooth_rgb_spectrum
from .snake import run as snake
from .sparkle import run as sparkle
from .swirling_candy_cane import run as swirling_candy_cane
# from .tetrahedron import run as tetrahedron
from .time_warp import run as time_warp
from .tree_ception import run as tree_ception
from .vertical_scan import run as vertical_scan
from .xmaslights_spin import run as xmaslights_spin

ANIMATIONS = [
    {
        "name": "Breathing Tree",
        "function": breathing_tree
    },
    {
        "name": "Minecraft Enchantment Glint",
        "function": enchantment_glint
    },
    {
        "name": "Fire",
        "function": fire
    },
    {
        "name": "Intersecting Planes",
        "function": intersecting_planes
    },
    {
        "name": "Rainbow Swirl",
        "function": rainbow_swirl
    },
    {
        "name": "Random Direction Scan",
        "function": random_direction_scan
    },
    {
        "name": "Random RGB All",
        "function": random_rgb_all
    },
    {
        "name": "RGB Spheres",
        "function": rgb_spheres
    },
    {
        "name": "Scrolling Text",
        "function": scrolling_text
    },
    {
        "name": "Smooth RGB Spectrum",
        "function": smooth_rgb_spectrum
    },
    {
        "name": "Snake",
        "function": snake
    },
    {
        "name": "Sparkle",
        "function": sparkle
    },
    {
        "name": "Swirling Candycane",
        "function": swirling_candy_cane
    },
    # {
    #     "name": "Tetrahedron",
    #     "function": tetrahedron
    # },
    {
        "name": "Time Warp",
        "function": time_warp
    },
    {
        "name": "Tree-ception",
        "function": tree_ception
    },
    {
        "name": "Vertical Scan",
        "function": vertical_scan
    },
    {
        "name": "Xmas Lights Spin",
        "function": xmaslights_spin
    }
]