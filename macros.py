from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mkdocs_macros.plugin import MacrosPlugin


def render_image(subfolder: str, filename: str, width: int) -> str:
    return f'<img src="site:images/{subfolder}/{filename}" width="{width}">'


IMAGE_WIDTH = 120


def define_env(env: "MacrosPlugin") -> None:
    @env.macro  # type: ignore[misc]
    def img_f2l(number: int) -> str:
        return render_image("f2l", f"F2L{number}.png", IMAGE_WIDTH)

    @env.macro  # type: ignore[misc]
    def img_oll(number: int) -> str:
        return render_image("oll", f"O{number}.png", IMAGE_WIDTH)

    @env.macro  # type: ignore[misc]
    def img_pll(letter: str) -> str:
        return render_image("pll", f"{letter}.webp", IMAGE_WIDTH)
