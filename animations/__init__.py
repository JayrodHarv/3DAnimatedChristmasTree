from .breathing_tree import BreathingTreeAnimation
from .enchantment_glint import EnchantmentGlintAnimation
from .fire import FireAnimation
from .gradient_sweep import GradientSweepAnimation
from .intersecting_planes import IntersectingPlanesAnimation
from .random_direction_scan import RandomDirectionScanAnimation
from .random_rgb_all import RandomRGBAllAnimation
from .rainbow_swirl import RainbowSwirlAnimation
from .rgb_spheres import RGBSpheresAnimation
from .scrolling_text import ScrollingTextAnimation
from .snake import SnakeAnimation
from .smooth_rgb_spectrum import SmoothRGBSpectrumAnimation
from .sparkle import SparkleAnimation
from .sweep import SweepAnimation
from .swirling_candy_cane import SwirlingCandyCaneAnimation
from .time_warp import TimeWarpAnimation
from .tree_ception import TreeCeptionAnimation
from .vertical_scan import VerticalScanAnimation
from .xmaslights_spin import XmasLightsSpinAnimation

def create_animations(coords, pixels):
    return [
        BreathingTreeAnimation(coords, pixels),
        EnchantmentGlintAnimation(coords, pixels),
        FireAnimation(coords, pixels),
        GradientSweepAnimation(coords, pixels),
        IntersectingPlanesAnimation(coords, pixels),
        RandomDirectionScanAnimation(coords, pixels),
        RandomRGBAllAnimation(coords, pixels),
        RainbowSwirlAnimation(coords, pixels),
        RGBSpheresAnimation(coords, pixels),
        ScrollingTextAnimation(coords, pixels),
        SnakeAnimation(coords, pixels),
        SmoothRGBSpectrumAnimation(coords, pixels),
        SparkleAnimation(coords, pixels),
        SweepAnimation(coords, pixels),
        SwirlingCandyCaneAnimation(coords, pixels),
        TimeWarpAnimation(coords, pixels),
        TreeCeptionAnimation(coords, pixels),
        VerticalScanAnimation(coords, pixels),
        XmasLightsSpinAnimation(coords, pixels),
    ]