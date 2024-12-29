from rubik import Movement, Rubik, parse_movements


def test_six_sexy_moves() -> None:
    rubik = Rubik()

    assert rubik.is_solved()

    for _ in range(6):
        rubik.move(Movement.R)
        rubik.move(Movement.U)
        rubik.move(Movement.R_PRIME)
        rubik.move(Movement.U_PRIME)

    assert rubik.is_solved()


def test_up_face() -> None:
    rubik = Rubik()

    assert rubik.is_solved()

    rubik.move(Movement.U)
    rubik.move(Movement.U_PRIME)

    assert rubik.is_solved()


def test_4_up_moves() -> None:
    rubik = Rubik()

    assert rubik.is_solved()

    rubik.move(Movement.U)
    rubik.move(Movement.U)
    rubik.move(Movement.U)
    rubik.move(Movement.U)

    assert rubik.is_solved()

    rubik.move(Movement.R, 4)

    assert rubik.is_solved()


def test_perm_ua() -> None:
    rubik = Rubik()

    assert rubik.is_solved()

    # perform perm ua 3 times, cube should be back to its initial position
    movements = parse_movements("R U R' U R' U' R2 U' R' U R' U R")

    for _ in range(3):
        for movement, number_of_moves in movements:
            rubik.move(movement, number_of_moves)

        rubik.move(Movement.U, 2)

    assert rubik.is_solved()


def test_perm_ua_alternative_algorithm() -> None:
    rubik = Rubik()

    assert rubik.is_solved()

    movements = parse_movements("M2' U M U2 M' U M2'")

    for _ in range(3):
        for movement, number_of_moves in movements:
            rubik.move(movement, number_of_moves)

    assert rubik.is_solved()


def test_perm_ub() -> None:
    rubik = Rubik()

    assert rubik.is_solved()

    movements = parse_movements("R' U R' U' R3 U' R' U R U R2")

    for _ in range(3):
        for movement, number_of_moves in movements:
            rubik.move(movement, number_of_moves)

    assert rubik.is_solved()


def test_perm_na() -> None:
    rubik = Rubik()

    assert rubik.is_solved()

    movements = parse_movements("R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'")

    for _ in range(2):
        for movement, number_of_moves in movements:
            rubik.move(movement, number_of_moves)

    assert rubik.is_solved()


def test_perm_nb() -> None:
    rubik = Rubik()

    assert rubik.is_solved()

    movements = parse_movements("(R' U R U' R') (F' U' F) (R U R') (F R' F') (R U' R)")

    for _ in range(2):
        for movement, number_of_moves in movements:
            rubik.move(movement, number_of_moves)

    assert rubik.is_solved()


def test_perm_ja() -> None:
    rubik = Rubik()

    assert rubik.is_solved()

    movements = parse_movements("L U' R' U L' U2 R U' R' U2 R")

    for _ in range(2):
        for movement, number_of_moves in movements:
            rubik.move(movement, number_of_moves)

    assert rubik.is_solved()


def test_perm_h() -> None:
    rubik = Rubik()

    assert rubik.is_solved()

    movements = parse_movements("M2' U M2' U2 M2' U M2'")

    for _ in range(2):
        for movement, number_of_moves in movements:
            rubik.move(movement, number_of_moves)

    assert rubik.is_solved()


def test_perm_dddd() -> None:
    rubik = Rubik()

    assert rubik.is_solved()

    movements = parse_movements("M2' U M U2 M' U M2'")

    for _ in range(3):
        for movement, number_of_moves in movements:
            rubik.move(movement, number_of_moves)

    assert rubik.is_solved()
