import pytest

from rubik_algorithm import CubeRotation, Rubik, parse_movements


@pytest.mark.parametrize(
    ("number_of_cycles", "algorithms", "auf"),
    [
        (6, "R U R' U'", None),
        (1, "U U'", None),
        (1, "U U U U", None),
        (1, "R4", None),
        (3, "R U R' U R' U' R2 U' R' U R' U R", "U2"),
        (3, "M2' U M U2 M' U M2'", None),
        (3, "R' U R' U' R3 U' R' U R U R2", None),
        (2, "R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'", None),
        (2, "(R' U R U' R') (F' U' F) (R U R') (F R' F') (R U' R)", None),
        (2, "r' D' F r U' r' F' D r2 U r' U' r' F r F'", None),
        (2, "L U' R' U L' U2 R U' R' U2 R", None),
        (2, "R U R' F' R U R' U' R' F R2 U' R' U'", None),
        (2, "M2' U M2' U2 M2' U M2'", None),
        (3, "R' D' R U' R' D R U2 R' D' R U' R' D R", None),
        (3, "S (R U R' U') (R' F R f')", None),
        (4, "y' R U' R2 D' r U r' D R2 U R'", None),
    ],
    ids=(
        "sexy moves",
        "up face",
        "4 up moves",
        "4 right moves",
        "perm ua",
        "perm ua alt",
        "perm ub",
        "perm na",
        "perm nb",
        "perm nb alt",
        "perm ja",
        "perm jb",
        "perm h",
        "perm aa",
        "oll 32",
        "oll 2",
    ),
)
def test_algorithms_cycle(number_of_cycles: int, algorithms: str, auf: str | None) -> None:
    rubik = Rubik()

    assert rubik.is_solved()

    movements = parse_movements(algorithms)

    # Remove initial cube rotation if any
    if isinstance(movements[0][0], CubeRotation):
        movements.pop(0)

    auf_movements = parse_movements(auf) if auf is not None else None

    for _ in range(number_of_cycles):
        for movement, number_of_moves in movements:
            rubik.move(movement, number_of_moves)

        if auf_movements is not None:
            for movement, number_of_moves in auf_movements:
                rubik.move(movement, number_of_moves)

    assert rubik.is_solved()
