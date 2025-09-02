import re
from copy import deepcopy
from enum import StrEnum
from textwrap import dedent
from typing import Any

import numpy as np
import numpy.typing as npt


class Color(StrEnum):
    RED = "RED"
    WHITE = "WHITE"
    GREEN = "GREEN"
    ORANGE = "ORANGE"
    YELLOW = "YELLOW"
    BLUE = "BLUE"


class Movement(StrEnum):
    R = "RIGHT"
    R_PRIME = "RIGHT_PRIME"
    L = "LEFT"
    L_PRIME = "LEFT_PRIME"
    F = "FRONT"
    F_PRIME = "FRONT_PRIME"
    B = "BACK"
    B_PRIME = "BACK_PRIME"
    U = "UP"
    U_PRIME = "UP_PRIME"
    D = "DOWN"
    D_PRIME = "DOWN_PRIME"
    M = "MIDDLE"
    M_PRIME = "MIDDLE_PRIME"
    S = "STANDING"
    S_PRIME = "STANDING_PRIME"

    r = "RIGHT_CENTRALE"
    r_PRIME = "RIGHT_PRIME_CENTRALE"
    f = "FRONT_CENTRALE"
    f_PRIME = "FRONT_PRIME_CENTRALE"


def opposite_color(color: Color) -> Color:
    map = {
        Color.WHITE: Color.YELLOW,
        Color.RED: Color.ORANGE,
        Color.GREEN: Color.BLUE,
    }

    inversed_map = {value: key for key, value in map.items()}

    return (map | inversed_map)[color]


def is_face_solved(face: npt.NDArray[np.str_]) -> bool:
    first_color: np.str_ = face[0, 0]

    return (face == first_color).all()  # type: ignore[no-any-return]


def clockwise_rotation(
    face: np.ndarray[tuple[int, ...], np.dtype[Any]],
) -> np.ndarray[tuple[int, ...], np.dtype[Any]]:
    return np.rot90(face, k=-1)


def counterclockwise_rotation(
    face: np.ndarray[tuple[int, ...], np.dtype[Any]],
) -> np.ndarray[tuple[int, ...], np.dtype[Any]]:
    return np.rot90(face)


def parse_movement(raw_movement: str) -> tuple[Movement, int]:
    regex = re.compile("([a-zA-Z])([0-9]?)('?)")

    search = re.search(regex, raw_movement)

    if search is None:
        raise ValueError(f"Could not parse movement: {raw_movement}")

    raw_dir = search.groups()[0]

    try:
        number_of_moves = int(search.groups()[1])
    except (IndexError, ValueError):
        number_of_moves = 1

    prime = search.groups()[2]

    map = {
        "R": Movement.R,
        "R'": Movement.R_PRIME,
        "L": Movement.L,
        "L'": Movement.L_PRIME,
        "F": Movement.F,
        "F'": Movement.F_PRIME,
        "B": Movement.B,
        "B'": Movement.B_PRIME,
        "U": Movement.U,
        "U'": Movement.U_PRIME,
        "D": Movement.D,
        "D'": Movement.D_PRIME,
        "M": Movement.M,
        "M'": Movement.M_PRIME,
        "S": Movement.S,
        "S'": Movement.S_PRIME,
        "r": Movement.r,
        "r'": Movement.r_PRIME,
        "f": Movement.f,
        "f'": Movement.f_PRIME,
    }

    return map[raw_dir + prime], number_of_moves


def parse_movements(raw_movements: str) -> list[tuple[Movement, int]]:
    return [
        parse_movement(raw_movement)
        for raw_movement in raw_movements.replace("(", "").replace(")", "").split()
    ]


class Rubik:
    def __init__(self) -> None:
        self.front_face = np.array(
            [
                [Color.YELLOW, Color.YELLOW, Color.YELLOW],
                [Color.YELLOW, Color.YELLOW, Color.YELLOW],
                [Color.YELLOW, Color.YELLOW, Color.YELLOW],
            ],
            Color,
        )
        self.right_face = np.array(
            [
                [Color.GREEN, Color.GREEN, Color.GREEN],
                [Color.GREEN, Color.GREEN, Color.GREEN],
                [Color.GREEN, Color.GREEN, Color.GREEN],
            ],
            Color,
        )
        self.left_face = np.array(
            [
                [Color.BLUE, Color.BLUE, Color.BLUE],
                [Color.BLUE, Color.BLUE, Color.BLUE],
                [Color.BLUE, Color.BLUE, Color.BLUE],
            ],
            Color,
        )
        self.up_face = np.array(
            [
                [Color.ORANGE, Color.ORANGE, Color.ORANGE],
                [Color.ORANGE, Color.ORANGE, Color.ORANGE],
                [Color.ORANGE, Color.ORANGE, Color.ORANGE],
            ],
            Color,
        )
        self.back_face = np.array(
            [
                [Color.WHITE, Color.WHITE, Color.WHITE],
                [Color.WHITE, Color.WHITE, Color.WHITE],
                [Color.WHITE, Color.WHITE, Color.WHITE],
            ],
            Color,
        )
        self.down_face = np.array(
            [
                [Color.RED, Color.RED, Color.RED],
                [Color.RED, Color.RED, Color.RED],
                [Color.RED, Color.RED, Color.RED],
            ],
            Color,
        )

    def is_valid(self) -> bool:
        return (
            {
                self.front_face[1, 1],
                self.back_face[1, 1],
                self.up_face[1, 1],
                self.down_face[1, 1],
                self.left_face[1, 1],
                self.right_face[1, 1],
            }
            == {Color.WHITE, Color.YELLOW, Color.RED, Color.GREEN, Color.BLUE, Color.ORANGE}
            and self.front_face[1, 1] == opposite_color(self.back_face[1, 1])
            and self.up_face[1, 1] == opposite_color(self.down_face[1, 1])
            and self.left_face[1, 1] == opposite_color(self.right_face[1, 1])
        )

    def is_solved(self) -> bool:
        return (
            self.is_valid()
            and is_face_solved(self.front_face)
            and is_face_solved(self.back_face)
            and is_face_solved(self.left_face)
            and is_face_solved(self.right_face)
            and is_face_solved(self.up_face)
            and is_face_solved(self.down_face)
        )

    def perform_up(self) -> None:
        self.up_face = clockwise_rotation(self.up_face)

        saved = deepcopy(self.front_face[0])
        self.front_face[0] = self.right_face[0]
        self.right_face[0] = self.back_face[0]
        self.back_face[0] = self.left_face[0]
        self.left_face[0] = saved

    def perform_up_prime(self) -> None:
        self.up_face = counterclockwise_rotation(self.up_face)

        saved = deepcopy(self.front_face[0])
        self.front_face[0] = self.left_face[0]
        self.left_face[0] = self.back_face[0]
        self.back_face[0] = self.right_face[0]
        self.right_face[0] = saved

    def perform_down(self) -> None:
        self.down_face = clockwise_rotation(self.down_face)

        saved = deepcopy(self.front_face[2])
        self.front_face[2] = self.left_face[2]
        self.left_face[2] = self.back_face[2]
        self.back_face[2] = self.right_face[2]
        self.right_face[2] = saved

    def perform_down_prime(self) -> None:
        self.down_face = counterclockwise_rotation(self.down_face)

        saved = deepcopy(self.front_face[2])
        self.front_face[2] = self.right_face[2]
        self.right_face[2] = self.back_face[2]
        self.back_face[2] = self.left_face[2]
        self.left_face[2] = saved

    def perform_left(self) -> None:
        self.left_face = clockwise_rotation(self.left_face)

        saved = deepcopy(self.front_face[:, 0])
        self.front_face[:, 0] = self.up_face[:, 0]
        self.up_face[:, 0] = self.back_face[:, 2][::-1]
        self.back_face[:, 2] = self.down_face[:, 0][::-1]
        self.down_face[:, 0] = saved

    def perform_left_prime(self) -> None:
        self.left_face = counterclockwise_rotation(self.left_face)

        saved = deepcopy(self.front_face[:, 0])
        self.front_face[:, 0] = self.down_face[:, 0]
        self.down_face[:, 0] = self.back_face[:, 2][::-1]
        self.back_face[:, 2] = self.up_face[:, 0][::-1]
        self.up_face[:, 0] = saved

    def perform_right(self) -> None:
        self.right_face = clockwise_rotation(self.right_face)

        saved = deepcopy(self.front_face[:, 2])
        self.front_face[:, 2] = self.down_face[:, 2]
        self.down_face[:, 2] = self.back_face[:, 0][::-1]
        self.back_face[:, 0] = self.up_face[:, 2][::-1]
        self.up_face[:, 2] = saved

    def perform_right_prime(self) -> None:
        self.right_face = counterclockwise_rotation(self.right_face)

        saved = deepcopy(self.front_face[:, 2])
        self.front_face[:, 2] = self.up_face[:, 2]
        self.up_face[:, 2] = self.back_face[:, 0][::-1]
        self.back_face[:, 0] = self.down_face[:, 2][::-1]
        self.down_face[:, 2] = saved

    def perform_front(self) -> None:
        self.front_face = clockwise_rotation(self.front_face)

        saved = deepcopy(self.up_face[2, :])
        self.up_face[2, :] = self.left_face[:, 2][::-1].transpose()
        self.left_face[:, 2] = self.down_face[0, :].transpose()
        self.down_face[0, :] = self.right_face[:, 0][::-1].transpose()
        self.right_face[:, 0] = saved.transpose()

    def perform_front_prime(self) -> None:
        self.front_face = counterclockwise_rotation(self.front_face)

        saved = deepcopy(self.up_face[2, :])
        self.up_face[2, :] = self.right_face[:, 0].transpose()
        self.right_face[:, 0] = self.down_face[0, :].transpose()[::-1]
        self.down_face[0, :] = self.left_face[:, 2].transpose()
        self.left_face[:, 2] = saved.transpose()[::-1]

    def perform_standing(self) -> None:
        saved = deepcopy(self.up_face[1, :])
        self.up_face[1, :] = self.left_face[:, 1][::-1].transpose()
        self.left_face[:, 1] = self.down_face[1, :][::-1].transpose()
        self.down_face[1, :] = self.right_face[:, 1][::-1].transpose()
        self.right_face[:, 1] = saved.transpose()

    def perform_standing_prime(self) -> None:
        saved = deepcopy(self.up_face[1, :])
        self.up_face[1, :] = self.right_face[:, 1].transpose()
        self.right_face[:, 1] = self.down_face[1, :].transpose()[::-1]
        self.down_face[1, :] = self.left_face[:, 1].transpose()
        self.left_face[:, 1] = saved.transpose()[::-1]

    def perform_middle(self) -> None:
        saved = deepcopy(self.front_face[:, 1])
        self.front_face[:, 1] = self.up_face[:, 1]
        self.up_face[:, 1] = self.back_face[:, 1][::-1]
        self.back_face[:, 1] = self.down_face[:, 1][::-1]
        self.down_face[:, 1] = saved

    def perform_middle_prime(self) -> None:
        saved = deepcopy(self.front_face[:, 1])
        self.front_face[:, 1] = self.down_face[:, 1]
        self.down_face[:, 1] = self.back_face[:, 1][::-1]
        self.back_face[:, 1] = self.up_face[:, 1][::-1]
        self.up_face[:, 1] = saved

    def move(self, movement: Movement, number_of_moves: int = 1) -> None:
        for _ in range(number_of_moves):
            if movement == Movement.D:
                self.perform_down()
            elif movement == Movement.D_PRIME:
                self.perform_down_prime()
            elif movement == Movement.U:
                self.perform_up()
            elif movement == Movement.U_PRIME:
                self.perform_up_prime()
            elif movement == Movement.R:
                self.perform_right()
            elif movement == Movement.R_PRIME:
                self.perform_right_prime()
            elif movement == Movement.F:
                self.perform_front()
            elif movement == Movement.F_PRIME:
                self.perform_front_prime()
            elif movement == Movement.L:
                self.perform_left()
            elif movement == Movement.L_PRIME:
                self.perform_left_prime()
            elif movement == Movement.M:
                self.perform_middle()
            elif movement == Movement.M_PRIME:
                self.perform_middle_prime()
            elif movement == Movement.S:
                self.perform_standing()
            elif movement == Movement.S_PRIME:
                self.perform_standing_prime()
            elif movement == Movement.r:
                self.perform_right()
                self.perform_middle_prime()
            elif movement == Movement.r_PRIME:
                self.perform_right_prime()
                self.perform_middle()
            elif movement == Movement.f:
                self.perform_front()
                self.perform_standing()
            elif movement == Movement.f_PRIME:
                self.perform_front_prime()
                self.perform_standing_prime()
            else:
                raise ValueError(f"Wrong movement: {movement}")


def compute_number_of_periods(raw_movement: str) -> int:
    rubik = Rubik()

    movements = parse_movements(raw_movement)

    period = 0

    while period == 0 or not rubik.is_solved():
        for movement, number_of_moves in movements:
            rubik.move(movement, number_of_moves)

        period += 1

    return period


def render_oll(index: int, movements: str) -> str:
    return dedent(f"""
        ### OLL {index}\n
        ![image info](img/O{index}.gif)\n
        Algorithm: {movements}\n
        Nombre de movements: {compute_number_of_periods(movements)}\n
    """)


def render_pll(index: int, movements: str) -> str:
    return dedent(f"""
        ### PLL {index}\n
        ![image info](img/P{index}.gif)\n
        Algorithm: {movements}\n
        Nombre de movements: {compute_number_of_periods(movements)}\n
    """)
