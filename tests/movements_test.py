import pytest

from rubik_algorithm import Movement, parse_movements


@pytest.mark.parametrize(
    ("raw_movements", "parsed_movements"),
    [
        (
            "(R' U R U' R') (F' U' F) (R U R') (F R' F') (R U' R)",
            [
                (Movement.R_PRIME, 1),
                (Movement.U, 1),
                (Movement.R, 1),
                (Movement.U_PRIME, 1),
                (Movement.R_PRIME, 1),
                (Movement.F_PRIME, 1),
                (Movement.U_PRIME, 1),
                (Movement.F, 1),
                (Movement.R, 1),
                (Movement.U, 1),
                (Movement.R_PRIME, 1),
                (Movement.F, 1),
                (Movement.R_PRIME, 1),
                (Movement.F_PRIME, 1),
                (Movement.R, 1),
                (Movement.U_PRIME, 1),
                (Movement.R, 1),
            ],
        ),
        (
            "M2' U M2' U2 M2' U M2'",
            [
                (Movement.M_PRIME, 2),
                (Movement.U, 1),
                (Movement.M_PRIME, 2),
                (Movement.U, 2),
                (Movement.M_PRIME, 2),
                (Movement.U, 1),
                (Movement.M_PRIME, 2),
            ],
        ),
    ],
    ids=("perm nb", "perm h"),
)
def test_movements(raw_movements: str, parsed_movements: list[tuple[Movement, int]]) -> None:
    assert parsed_movements == parse_movements(raw_movements)
