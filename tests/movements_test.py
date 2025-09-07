import pytest

from rubik_algorithm import FaceRotation, parse_movements


@pytest.mark.parametrize(
    ("raw_movements", "parsed_movements"),
    [
        (
            "(R' U R U' R') (F' U' F) (R U R') (F R' F') (R U' R)",
            [
                (FaceRotation.R_PRIME, 1),
                (FaceRotation.U, 1),
                (FaceRotation.R, 1),
                (FaceRotation.U_PRIME, 1),
                (FaceRotation.R_PRIME, 1),
                (FaceRotation.F_PRIME, 1),
                (FaceRotation.U_PRIME, 1),
                (FaceRotation.F, 1),
                (FaceRotation.R, 1),
                (FaceRotation.U, 1),
                (FaceRotation.R_PRIME, 1),
                (FaceRotation.F, 1),
                (FaceRotation.R_PRIME, 1),
                (FaceRotation.F_PRIME, 1),
                (FaceRotation.R, 1),
                (FaceRotation.U_PRIME, 1),
                (FaceRotation.R, 1),
            ],
        ),
        (
            "M2' U M2' U2 M2' U M2'",
            [
                (FaceRotation.M_PRIME, 2),
                (FaceRotation.U, 1),
                (FaceRotation.M_PRIME, 2),
                (FaceRotation.U, 2),
                (FaceRotation.M_PRIME, 2),
                (FaceRotation.U, 1),
                (FaceRotation.M_PRIME, 2),
            ],
        ),
    ],
    ids=("perm nb", "perm h"),
)
def test_movements(raw_movements: str, parsed_movements: list[tuple[FaceRotation, int]]) -> None:
    assert parsed_movements == parse_movements(raw_movements)
