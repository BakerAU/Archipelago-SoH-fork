from Options import Accessibility
from ..Options import SohOptions, RainbowBridge, GanonsCastleBossKey, ShuffleTokens
from ..Locations import token_amounts
from ..Enums import TokenCounts
import pytest
from typing import cast
from types import SimpleNamespace

class TestSohOptions:

    def __init__(self):
        # These are picked to avoid the conditions we're testing for to make it easier to isolate
        # conditional logics in the tests
        self.shuffle_100_gs_reward = False
        self.accessibility = Accessibility.option_full
        self.exclude_locations = set()

        self.rainbow_bridge = RainbowBridge.option_vanilla
        self.rainbow_bridge_skull_tokens_required = SimpleNamespace(value=0)

        self.ganons_castle_boss_key = GanonsCastleBossKey.option_vanilla
        self.ganons_castle_boss_key_skull_tokens_required = SimpleNamespace(value=0)

        self.shuffle_skull_tokens = ShuffleTokens.option_off
    
    def set_rainbow_bridge_tokens(self, amount):
        self.rainbow_bridge = RainbowBridge.option_tokens
        self.rainbow_bridge_skull_tokens_required.value = amount

    def set_ganons_castle_key_tokens(self, amount):
        self.ganons_castle_boss_key = GanonsCastleBossKey.option_lacs_skull_tokens
        self.ganons_castle_boss_key_skull_tokens_required.value = amount
    
    def calculate_progression_skulltula_count(self):
        return SohOptions.calculate_progression_skulltula_count(
            cast(SohOptions, self), 
            token_reward_counts=token_amounts
        )

@pytest.fixture
def options():
    return TestSohOptions()

def test_base_case(options):
    assert options.calculate_progression_skulltula_count() == 0

def test_100_gs_reward(options):
    options.shuffle_100_gs_reward = True
    assert options.calculate_progression_skulltula_count() == 0

def test_excludes_first_location(options):
    keys = list(token_amounts.keys())
    options.exclude_locations = {str(keys[0])}

    assert options.calculate_progression_skulltula_count() == 0

def test_rainbow_bridge_tokens(options):
    options.set_rainbow_bridge_tokens(80)
    assert options.calculate_progression_skulltula_count() == 0

def test_ganons_castle_tokens(options):
    options.set_ganons_castle_key_tokens(70)
    assert options.calculate_progression_skulltula_count() == 0

def test_max_requirement_used(options):
    options.set_rainbow_bridge_tokens(80)
    options.set_ganons_castle_key_tokens(90)

    assert options.calculate_progression_skulltula_count() == 0

def test_shuffle_all_tokens(options):
    options.shuffle_skull_tokens = ShuffleTokens.option_all
    assert options.calculate_progression_skulltula_count() == 50

def test_shuffle_overworld_tokens(options):
    options.shuffle_skull_tokens = ShuffleTokens.option_overworld
    assert options.calculate_progression_skulltula_count() == 6

def test_partial_shuffle_with_requirement(options):
    options.set_rainbow_bridge_tokens(80)
    options.shuffle_skull_tokens = ShuffleTokens.option_dungeon

    assert options.calculate_progression_skulltula_count() == 24

def test_shuffle_all_with_high_requirement(options):
    options.set_rainbow_bridge_tokens(80)
    options.shuffle_skull_tokens = ShuffleTokens.option_all

    assert options.calculate_progression_skulltula_count() == 80

def test_zero_when_requirement_fully_covered(options):
    options.set_rainbow_bridge_tokens(10)
    assert options.calculate_progression_skulltula_count() == 0

def test_caps_at_100(options):
    options.shuffle_100_gs_reward = True
    options.shuffle_skull_tokens = ShuffleTokens.option_all

    assert options.calculate_progression_skulltula_count() == 100

def test_minimal_accessibility_all_tokens(options):
    options.accessibility = Accessibility.option_minimal
    options.shuffle_skull_tokens = ShuffleTokens.option_all

    assert options.calculate_progression_skulltula_count() == 100

def test_minimal_accessibility_dungeon_tokens(options):
    options.accessibility = Accessibility.option_minimal
    options.shuffle_skull_tokens = ShuffleTokens.option_dungeon

    assert options.calculate_progression_skulltula_count() == TokenCounts.DUNGEON

def test_minimal_accessibility_overworld_tokens(options):
    options.accessibility = Accessibility.option_minimal
    options.shuffle_skull_tokens = ShuffleTokens.option_overworld

    assert options.calculate_progression_skulltula_count() == TokenCounts.OVERWORLD

def test_shuffle_count_is_ceiling_for_tokens(options):
    options.set_rainbow_bridge_tokens(100)
    options.shuffle_skull_tokens = ShuffleTokens.option_dungeon

    result = options.calculate_progression_skulltula_count()

    assert result == TokenCounts.DUNGEON

def test_no_shuffle_tokens(options):
    options.shuffle_skull_tokens = ShuffleTokens.option_off
    assert options.calculate_progression_skulltula_count() == 0