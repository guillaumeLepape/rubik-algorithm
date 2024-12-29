from rubik import Movement, parse_movements


def test_movements_perm_nb() -> None:
    movements = parse_movements("(R' U R U' R') (F' U' F) (R U R') (F R' F') (R U' R)")

    assert movements == [
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
    ]


def test_movements_perm_h() -> None:
    movements = parse_movements("M2' U M2' U2 M2' U M2'")

    assert movements == [
        (
            Movement.M_PRIME,
            2,
        ),
        (
            Movement.U,
            1,
        ),
        (
            Movement.M_PRIME,
            2,
        ),
        (
            Movement.U,
            2,
        ),
        (
            Movement.M_PRIME,
            2,
        ),
        (
            Movement.U,
            1,
        ),
        (
            Movement.M_PRIME,
            2,
        ),
    ]
