from .breathing_tree import run as breathing_tree
from .enchantment_glint import run as enchantment_glint
from .fire import run as fire
from .rainbow_swirl import run as rainbow_swirl
from .random_direction_scan import run as random_direction_scan
from .scrolling_text import run as scrolling_text
from .smooth_rgb_spectrum import run as smooth_rgb_spectrum
from .sparkle import run as sparkle
from .swirling_candy_cane import run as swirling_candy_cane
from .time_warp import run as time_warp
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
        "name": "Rainbow Swirl",
        "function": rainbow_swirl
    },
    {
        "name": "Random Direction Scan",
        "function": random_direction_scan
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
        "name": "Sparkle",
        "function": sparkle
    },
    {
        "name": "Swirling Candycane",
        "function": swirling_candy_cane
    },
    {
        "name": "Time Warp",
        "function": time_warp
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