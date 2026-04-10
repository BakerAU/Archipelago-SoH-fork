from .bases import SohTestBase
from Options import Accessibility, ExcludeLocations
from ..Options import SohOptions, Shuffle100GSReward, RainbowBridge, GanonsCastleBossKey, ShuffleTokens

class TestProgressiveSkulltulaCalculations(SohTestBase):
    options = {
        "shuffle_100_gs_reward": Shuffle100GSReward, 
        "accessibility": Accessibility.option_full, 
        "exclude_locations": ExcludeLocations,
        "rainbow_bridge": RainbowBridge.option_tokens,
        "ganons_castle_boss_key": GanonsCastleBossKey.option_lacs_skull_tokens,
        "shuffle_skull_tokens": ShuffleTokens.option_off
    }

    def test_100_gs_reward_shuffle(self):
        assert SohOptions.calculate_progressive_skulltula_count() == 100