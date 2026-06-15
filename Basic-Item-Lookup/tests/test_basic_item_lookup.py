# Importing functions to test from main program
from basic_item_lookup import format_coins, validate_input

# CURRENT TESTS --
# Formatting coins tests for different input values
# Validating input for item ID
def test_format_coins_zero():
    assert format_coins(0) == "0g 0s 0c"


def test_format_coins_copper_only():
    assert format_coins(99) == "0g 0s 99c"


def test_format_coins_silver_and_copper():
    assert format_coins(150) == "0g 1s 50c"


def test_format_coins_gold_silver_and_copper():
    assert format_coins(12345) == "1g 23s 45c"


def test_validate_input_accepts_numeric_string():
    assert validate_input("19721") is True


def test_validate_input_rejects_text():
    assert validate_input("ectoplasm") is False