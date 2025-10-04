from functools import partial
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mkdocs_macros.plugin import MacrosPlugin


def render_image(subfolder: str, filename: str, width: int) -> str:
    return f'<img src="site:images/{subfolder}/{filename}" width="{width}">'


def render_f2l_tab(tab_title: str, algorithms: list[tuple[str, str]]) -> list[str]:
    lines: list[str] = []

    lines.append(f"/// tab | {tab_title}")
    lines.append("")

    for algo_name, algo in algorithms:
        lines.append(f"**{algo_name}**")
        lines.append("")
        lines.append("```text")
        lines.append(f"{algo}")
        lines.append("```")

    lines.append("///")
    lines.append("")

    return lines


front_right_tab = partial(render_f2l_tab, "Front Right")
front_left_tab = partial(render_f2l_tab, "Front Left")
back_left_tab = partial(render_f2l_tab, "Back Left")
back_right_tab = partial(render_f2l_tab, "Back Right")


IMAGE_WIDTH = 120


def define_env(env: "MacrosPlugin") -> None:
    @env.macro  # type: ignore[misc]
    def img_oll(number: int) -> str:
        return render_image("oll", f"O{number}.png", IMAGE_WIDTH)

    @env.macro  # type: ignore[misc]
    def img_pll(letter: str) -> str:
        return render_image("pll", f"{letter}.webp", IMAGE_WIDTH)

    @env.macro  # type: ignore[misc]
    def render_f2l(
        number: int,
        setup_algorithm: str,
        front_right: list[tuple[str, str]],
        front_left: list[tuple[str, str]],
        back_left: list[tuple[str, str]],
        back_right: list[tuple[str, str]],
    ) -> str:
        lines: list[str] = []

        lines.append(f"**Setup**: {setup_algorithm}")
        lines.append("")
        lines.append(render_image("f2l", f"F2L{number}.png", IMAGE_WIDTH))
        lines.append("")

        lines.extend(front_right_tab(front_right))
        lines.extend(front_left_tab(front_left))
        lines.extend(back_left_tab(back_left))
        lines.extend(back_right_tab(back_right))

        return "\n".join(lines)
