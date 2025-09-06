from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).parents[1]


@pytest.mark.parametrize(
    ("folder", "file_prefix", "file_extension", "count"),
    [
        ("oll", "O", "png", 57),
        ("pll", "", "webp", 21),
    ],
)
def test_images(folder: str, file_prefix: str, file_extension: str, count: int) -> None:
    assert (
        len(list((ROOT_DIR / "docs" / "images" / folder).glob(f"{file_prefix}*.{file_extension}")))
        == count
    )
