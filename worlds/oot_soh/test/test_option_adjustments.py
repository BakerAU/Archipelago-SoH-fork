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
        self.accessibility = Accessibility.option_minimal
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

def test_100_gs_reward_forces_100(options):
    options.shuffle_100_gs_reward = True
    options.set_rainbow_bridge_tokens(80)

    assert options.calculate_progressive_skulltula_count() == 100

def test_full_accessibility_returns_50(options):
    options.accessibility = Accessibility.option_full

    assert options.calculate_progressive_skulltula_count() == 50

def test_uses_first_token_reward(options):
    expected = next(iter(token_amounts.values()))

    assert options.calculate_progressive_skulltula_count() == expected

def test_skips_excluded_first_location(options):
    keys = list(token_amounts.keys())
    values = list(token_amounts.values())

    options.exclude_locations = {str(keys[0])}

    assert options.calculate_progressive_skulltula_count() == values[1]

def test_skips_multiple_excluded_locations(options):
    keys = list(token_amounts.keys())
    values = list(token_amounts.values())

    options.exclude_locations = {str(keys[0]), str(keys[1])}

    assert options.calculate_progressive_skulltula_count() == values[2]

def test_rainbow_bridge_tokens_used(options):
    options.set_rainbow_bridge_tokens(80)

    assert options.calculate_progressive_skulltula_count() == 80

def test_rainbow_bridge_overrides_turn_in(options):
    options.set_rainbow_bridge_tokens(80)

    assert options.calculate_progressive_skulltula_count() == 80

def test_ganons_castle_key_tokens_used(options):
    options.set_ganons_castle_key_tokens(70)

    assert options.calculate_progressive_skulltula_count() == 70

def test_ganons_castle_key_overrides_turn_in(options):
    options.set_ganons_castle_key_tokens(70)

    assert options.calculate_progressive_skulltula_count() == 70

def test_returns_max_of_bridge_and_boss_key(options):
    options.set_rainbow_bridge_tokens(80)
    options.set_ganons_castle_key_tokens(70)

    assert options.calculate_progressive_skulltula_count() == 80

def test_returns_max_of_all_sources(options):
    options.set_rainbow_bridge_tokens(80)
    options.set_ganons_castle_key_tokens(90)

    assert options.calculate_progressive_skulltula_count() == 90

def test_shuffle_all_tokens_returns_100(options):
    options.shuffle_skull_tokens = ShuffleTokens.option_all

    assert options.calculate_progressive_skulltula_count() == 100

def test_shuffle_dungeon_tokens(options):
    options.shuffle_skull_tokens = ShuffleTokens.option_dungeon

    assert options.calculate_progressive_skulltula_count() == 50

def test_shuffle_overworld_tokens(options):
    options.shuffle_skull_tokens = ShuffleTokens.option_overworld

    assert options.calculate_progressive_skulltula_count() == int(TokenCounts.OVERWORLD)

def test_requirement_beats_shuffle(options):
    options.shuffle_skull_tokens = ShuffleTokens.option_dungeon
    options.set_rainbow_bridge_tokens(80)

    assert options.calculate_progressive_skulltula_count() == 80

def test_shuffle_beats_smaller_requirement(options):
    options.shuffle_skull_tokens = ShuffleTokens.option_all
    options.set_rainbow_bridge_tokens(80)

    assert options.calculate_progressive_skulltula_count() == 100


