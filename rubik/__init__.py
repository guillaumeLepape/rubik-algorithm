import re
from copy import deepcopy
from enum import StrEnum
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

    return (face == first_color).all()


def clockwise_rotation(
    face: np.ndarray[tuple[int, ...], np.dtype[Any]],
) -> np.ndarray[tuple[int, ...], np.dtype[Any]]:
    return np.rot90(face, k=-1)


def counterclockwise_rotation(
    face: np.ndarray[tuple[int, ...], np.dtype[Any]],
) -> np.ndarray[tuple[int, ...], np.dtype[Any]]:
    return np.rot90(face)


def parse_movement(raw_movement: str) -> tuple[Movement, int]:
    regex = re.compile("([A-Z])([0-9]?)('?)")

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

    def move(self, movement: Movement, number_of_moves: int = 1) -> None:
        for _ in range(number_of_moves):
            if movement == Movement.U:
                self.up_face = clockwise_rotation(self.up_face)

                saved = deepcopy(self.front_face[0])
                self.front_face[0] = self.right_face[0]
                self.right_face[0] = self.back_face[0]
                self.back_face[0] = self.left_face[0]
                self.left_face[0] = saved

            elif movement == Movement.U_PRIME:
                self.up_face = counterclockwise_rotation(self.up_face)

                saved = deepcopy(self.front_face[0])
                self.front_face[0] = self.left_face[0]
                self.left_face[0] = self.back_face[0]
                self.back_face[0] = self.right_face[0]
                self.right_face[0] = saved

            elif movement == Movement.R:
                self.right_face = clockwise_rotation(self.right_face)

                saved = deepcopy(self.front_face[:, 2])
                self.front_face[:, 2] = self.down_face[:, 2]
                self.down_face[:, 2] = self.back_face[:, 0][::-1]
                self.back_face[:, 0] = self.up_face[:, 2][::-1]
                self.up_face[:, 2] = saved

            elif movement == Movement.R_PRIME:
                self.right_face = counterclockwise_rotation(self.right_face)

                saved = deepcopy(self.front_face[:, 2])
                self.front_face[:, 2] = self.up_face[:, 2]
                self.up_face[:, 2] = self.back_face[:, 0][::-1]
                self.back_face[:, 0] = self.down_face[:, 2][::-1]
                self.down_face[:, 2] = saved

            elif movement == Movement.F:
                self.front_face = clockwise_rotation(self.front_face)

                saved = deepcopy(self.up_face[2, :])
                self.up_face[2, :] = self.left_face[:, 2][::-1].transpose()
                self.left_face[:, 2] = self.down_face[0, :].transpose()
                self.down_face[0, :] = self.right_face[:, 0][::-1].transpose()
                self.right_face[:, 0] = saved.transpose()

            elif movement == Movement.F_PRIME:
                self.front_face = counterclockwise_rotation(self.front_face)

                saved = deepcopy(self.up_face[2, :])
                self.up_face[2, :] = self.right_face[:, 0].transpose()
                self.right_face[:, 0] = self.down_face[0, :].transpose()[::-1]
                self.down_face[0, :] = self.left_face[:, 2].transpose()
                self.left_face[:, 2] = saved.transpose()[::-1]

            elif movement == Movement.L:
                self.left_face = clockwise_rotation(self.left_face)

                saved = deepcopy(self.front_face[:, 0])
                self.front_face[:, 0] = self.up_face[:, 0]
                self.up_face[:, 0] = self.back_face[:, 2][::-1]
                self.back_face[:, 2] = self.down_face[:, 0][::-1]
                self.down_face[:, 0] = saved

            elif movement == Movement.L_PRIME:
                self.left_face = counterclockwise_rotation(self.left_face)

                saved = deepcopy(self.front_face[:, 0])
                self.front_face[:, 0] = self.down_face[:, 0]
                self.down_face[:, 0] = self.back_face[:, 2][::-1]
                self.back_face[:, 2] = self.up_face[:, 0][::-1]
                self.up_face[:, 0] = saved

            elif movement == Movement.M:
                saved = deepcopy(self.front_face[:, 1])
                self.front_face[:, 1] = self.up_face[:, 1]
                self.up_face[:, 1] = self.back_face[:, 1][::-1]
                self.back_face[:, 1] = self.down_face[:, 1][::-1]
                self.down_face[:, 1] = saved

            elif movement == Movement.M_PRIME:
                saved = deepcopy(self.front_face[:, 1])
                self.front_face[:, 1] = self.down_face[:, 1]
                self.down_face[:, 1] = self.back_face[:, 1][::-1]
                self.back_face[:, 1] = self.up_face[:, 1][::-1]
                self.up_face[:, 1] = saved

            else:
                raise ValueError(f"Wrong movement: {movement}")
