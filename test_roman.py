import pytest
from roman import roman


@pytest.mark.weight_5
@pytest.mark.visibility_hidden
@pytest.mark.number_1
def test_one():
	assert roman(1) == 'I'


@pytest.mark.weight_3
@pytest.mark.number_2
@pytest.mark.name_Test_roman_numeral_II
def test_two():
	assert roman(2) == 'II'
