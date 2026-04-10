from .bases import SohTestBase
from Options import Accessibility, ExcludeLocations
from ..Options import SohOptions, Shuffle100GSReward, RainbowBridge, GanonsCastleBossKey, ShuffleTokens
from ..Locations import token_amounts
import pytest
from typing import cast

class TestSohOptions:

    def __init__(self):
        # These are picked to avoid the conditions we're testing for to make it easier to isolate
        # conditional logics in the tests
        self.shuffle_100_gs_reward = False
        self.accessibility = Accessibility.option_minimal
        self.exclude_locations = set()

        self.rainbow_bridge = RainbowBridge.option_vanilla
        self.rainbow_bridge_skull_tokens_required = 0

        self.ganons_castle_boss_key = GanonsCastleBossKey.option_vanilla
        self.ganons_castle_boss_key_skull_tokens_required = 0

        self.shuffle_skull_tokens = ShuffleTokens.option_off
    
    def set_rainbow_bridge_tokens(self, amount):
        self.rainbow_bridge = RainbowBridge.option_tokens
        self.rainbow_bridge_skull_tokens_required= amount

    def set_ganons_castle_key_tokens(self, amount):
        self.ganons_castle_boss_key = GanonsCastleBossKey.option_lacs_skull_tokens
        self.ganons_castle_boss_key_skull_tokens_required = amount
    
    def calculate_progressive_skulltula_count(self):
        return SohOptions.calculate_progressive_skulltula_count(
            cast(SohOptions, self), 
            token_reward_counts=token_amounts
        )


@pytest.fixture
def options():
    return TestSohOptions()

def test_base_case(options):
    assert options.calculate_progressive_skulltula_count() == 50
