import re
from fractions import Fraction
from pathlib import Path


def test_oll_probability() -> None:
    file_content = (Path(__file__).parents[1] / "docs" / "oll.md").read_text()

    pattern = re.compile(r"Probability: \*\*([0-9]*)/([0-9]*)\*\*")

    matches = pattern.findall(file_content)

    assert len(matches) == 57

    sum_probabilities = Fraction(0)

    for numerator, denominator in matches:
        sum_probabilities += Fraction(int(numerator), int(denominator))

    probability_to_be_solved = Fraction(1, 216)

    assert sum_probabilities + probability_to_be_solved == 1
