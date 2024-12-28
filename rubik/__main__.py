from . import Rubik, parse_movements

if __name__ == "__main__":
    rubik = Rubik()

    movements = parse_movements("F' (L' U' L U) (L' U' L U) F")

    period = 0

    while period == 0 or not rubik.is_solved():
        for movement, number_of_moves in movements:
            rubik.move(movement, number_of_moves)

        period += 1

    print(period)

    print(rubik.is_solved())
