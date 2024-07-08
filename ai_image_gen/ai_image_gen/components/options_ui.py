import reflex as rx
from .. import styles
from ..backend.options import OptionsState
from ..backend.generation import GeneratorState


def sidebar_header() -> rx.Component:
    return rx.hstack(
        rx.link(
            rx.color_mode_cond(
                rx.image(src="/reflex_black.svg", height="1.15em", width="auto"),
                rx.image(src="/reflex_white.svg", height="1.15em", width="auto"),
            ),
            href="https://reflex.dev",
            is_external=True,
            padding="0",
        ),
        rx.spacer(),
        rx.color_mode.button(
            style={"padding": "0", "height": "1.15em", "width": "1.15em"},
        ),
        align="center",
        width="100%",
        border_bottom=styles.border,
        padding="1em",
    )


def mobile_header() -> rx.Component:
    return rx.hstack(
        rx.link(
            rx.color_mode_cond(
                rx.image(src="/reflex_black.svg", height="1em", width="auto"),
                rx.image(src="/reflex_white.svg", height="1em", width="auto"),
            ),
            href="https://reflex.dev",
            is_external=True,
            padding="0",
        ),
        rx.spacer(),
        rx.color_mode.button(
            style={"padding": "0", "height": "1.25em", "width": "1.25em"},
        ),
        display=["flex", "flex", "flex", "none"],
        justify="end",
        id="mobile-header",
        border_bottom=styles.border,
        align="center",
        width="100%",
        padding="1em",
    )


def prompt_input() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("type", size=17, color=rx.color("green", 9)),
            rx.text("Prompt", size="3"),
            rx.spacer(),
            rx.hstack(
                rx.cond(
                    OptionsState.prompt,
                    rx.icon(
                        "eraser",
                        size=20,
                        color=rx.color("gray", 10),
                        cursor="pointer",
                        _hover={"opacity": "0.8"},
                        on_click=OptionsState.setvar("prompt", ""),
                    ),
                ),
                rx.tooltip(
                    rx.box(  # Without the box the tooltip is not visible
                        rx.icon(
                            "dices",
                            size=20,
                            color=rx.color("gray", 10),
                            cursor="pointer",
                            _hover={"opacity": "0.8"},
                            on_click=OptionsState.randomize_prompt,
                        ),
                    ),
                    content="Randomize prompt",
                ),
                spacing="4",
                align="center",
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        rx.text_area(
            placeholder="What do you want to see?",
            width="100%",
            size="3",
            value=OptionsState.prompt,
            on_change=OptionsState.set_prompt,
        ),
        width="100%",
    )


def _create_arrow_icon(
    direction: str = "",
    top: str = "",
    left: str = "",
    right: str = "",
    bottom: str = "",
) -> rx.Component:
    return rx.icon(
        direction,
        size=17,
        color=rx.color("gray", 10),
        position="absolute",
        top=top,
        left=left,
        right=right,
        bottom=bottom,
    )


def size_selector() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("scan", size=17, color=rx.color("orange", 9)),
            rx.text("Dimensions", size="3"),
            spacing="2",
            align="center",
            width="100%",
        ),
        rx.vstack(
            rx.slider(
                min=0,
                max=(OptionsState.dimensions).length() - 1,
                step=1,
                size="1",
                default_value=OptionsState.slider_tick,
                on_change=OptionsState.set_tick,
                on_blur=OptionsState.set_hover(False),
                on_mouse_enter=OptionsState.set_hover(True),
                on_mouse_leave=OptionsState.set_hover(False),
            ),
            rx.hstack(
                rx.icon("rectangle-horizontal", size=22, color=rx.color("gray", 9)),
                rx.center(
                    rx.flex(
                        rx.text(
                            OptionsState.dimensions_str,
                            size="2",
                            justify="center",
                            align="center",
                        ),
                        _create_arrow_icon("arrow-up-left", top="2.5px", left="2.5px"),
                        _create_arrow_icon(
                            "arrow-up-right", top="2.5px", right="2.5px"
                        ),
                        _create_arrow_icon(
                            "arrow-down-left", bottom="2.5px", left="2.5px"
                        ),
                        _create_arrow_icon(
                            "arrow-down-right", bottom="2.5px", right="2.5px"
                        ),
                        width=OptionsState.dimensions[OptionsState.slider_tick][0] // 8,
                        height=OptionsState.dimensions[OptionsState.slider_tick][1]
                        // 8,
                        bg=rx.color("gray", 7),
                        padding="2.5px",
                        justify="center",
                        align="center",
                        position="relative",
                        transition="all 0.1s ease",
                        border="1.5px solid var(--gray-9)",
                        box_shadow=styles.box_shadow,
                        style={
                            "transition": "opacity 0.3s ease-out, transform 0.3s ease-out, visibility 0.3s ease-out",
                            "opacity": rx.cond(OptionsState.hover, "1", "0"),
                            "visibility": rx.cond(
                                OptionsState.hover, "visible", "hidden"
                            ),
                            "transform": rx.cond(
                                OptionsState.hover, "scale(1)", "scale(0)"
                            ),
                        },
                    ),
                    position="absolute",
                    transform="translate(0%, 45%)",
                    width="100%",
                    z_index=rx.cond(OptionsState.hover, "500", "0"),
                ),
                rx.text(
                    OptionsState.dimensions_str,
                    size="2",
                    style={
                        "transition": "opacity 0.15s ease-out, visibility 0.15s ease-out",
                        "visibility": rx.cond(OptionsState.hover, "hidden", "visible"),
                        "opacity": rx.cond(OptionsState.hover, "0", "1"),
                    },
                ),
                rx.icon("rectangle-vertical", size=22, color=rx.color("gray", 9)),
                position="relative",
                justify="between",
                align="center",
                width="100%",
            ),
            width="100%",
        ),
        width="100%",
    )


def output_selector() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("image", size=17, color=rx.color("crimson", 9)),
            rx.text("Image count", size="3"),
            rx.spacer(),
            rx.text(f"{OptionsState.num_outputs}", size="3"),
            spacing="2",
            align="center",
            width="100%",
        ),
        rx.slider(
            min=1,
            max=4,
            step=1,
            size="1",
            default_value=OptionsState.num_outputs,
            on_change=OptionsState.set_num_outputs,
        ),
        width="100%",
    )


def _style_preview(style_preset: list) -> rx.Component:
    return rx.cond(
        style_preset[0] == OptionsState.selected_style,
        rx.tooltip(
            rx.box(
                rx.image(
                    src=style_preset[1]["path"],
                    width="100%",
                    height="auto",
                    decoding="async",
                    loading="lazy",
                    transition="all 0.2s ease",
                    style={
                        "transform": "scale(0.875)",
                    },
                ),
                width="110px",
                height="auto",
                cursor="pointer",
                background=rx.color("accent", 9),
                on_click=OptionsState.setvar("selected_style", ""),
            ),
            content=style_preset[0],
        ),
        rx.tooltip(
            rx.box(
                rx.image(
                    src=style_preset[1]["path"],
                    width="100%",
                    height="auto",
                    decoding="auto",
                    loading="lazy",
                    transition="all 0.2s ease",
                ),
                width="110px",
                height="auto",
                cursor="pointer",
                background=rx.color("accent", 9),
                on_click=OptionsState.setvar("selected_style", style_preset[0]),
            ),
            content=style_preset[0],
        ),
    )


def style_selector() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("palette", size=17, color=rx.color("indigo", 9)),
            rx.text(f"Style", size="3"),
            rx.spacer(),
            rx.cond(
                OptionsState.selected_style,
                rx.hstack(
                    rx.text(f"[ {OptionsState.selected_style} ]", size="3"),
                    rx.icon(
                        "eraser",
                        size=20,
                        color=rx.color("gray", 10),
                        cursor="pointer",
                        _hover={"opacity": "0.8"},
                        on_click=OptionsState.setvar("selected_style", ""),
                    ),
                    spacing="4",
                    align="center",
                ),
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        rx.scroll_area(
            rx.hstack(
                rx.foreach(
                    OptionsState.styles_preset,
                    _style_preview,
                ),
                width="100%",
                align="center",
                padding_bottom="15px",
            ),
            scrollbars="horizontal",
            height="100%",
            width="100%",
            type="always",
        ),
        width="100%",
    )


def _negative_prompt() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("type", size=17, color=rx.color("red", 9)),
            rx.text("Negative Prompt", size="3"),
            rx.tooltip(
                rx.icon(
                    "info",
                    size=15,
                    color=rx.color("gray", 10),
                ),
                content="Things you want to avoid in the image",
            ),
            rx.spacer(),
            rx.hstack(
                rx.cond(
                    OptionsState.negative_prompt,
                    rx.icon(
                        "eraser",
                        size=20,
                        color=rx.color("gray", 10),
                        cursor="pointer",
                        _hover={"opacity": "0.8"},
                        on_click=OptionsState.setvar("negative_prompt", ""),
                    ),
                ),
                spacing="4",
                align="center",
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        rx.text_area(
            placeholder="What do you want to avoid?",
            width="100%",
            size="3",
            value=OptionsState.negative_prompt,
            on_change=OptionsState.set_negative_prompt,
        ),
        width="100%",
    )


def _seed_input() -> rx.Component:
    return (
        rx.vstack(
            rx.hstack(
                rx.icon("sprout", size=17, color=rx.color("grass", 10)),
                rx.text("Seed", size="3"),
                rx.spacer(),
                rx.hstack(
                    rx.cond(
                        OptionsState.seed > 0,
                        rx.icon(
                            "eraser",
                            size=20,
                            color=rx.color("gray", 10),
                            cursor="pointer",
                            _hover={"opacity": "0.8"},
                            on_click=OptionsState.setvar("seed", 0),
                        ),
                    ),
                    spacing="4",
                    align="center",
                ),
                spacing="2",
                align="center",
                width="100%",
            ),
            rx.tooltip(
                rx.box(
                    rx.input(
                        type="number",
                        value=OptionsState.seed,
                        on_change=OptionsState.set_seed,
                        placeholder="0 (Auto)",
                        max_length=5,
                        width="100%",
                    ),
                    width="100%",
                ),
                content="A number that determines the randomness of the image. Use the same seed to get the same result every time. 0 = Auto",
                side="right",
            ),
            spacing="2",
        ),
    )


def _scheduler_input() -> rx.Component:
    return (
        rx.vstack(
            rx.hstack(
                rx.icon("align-left", size=17, color=rx.color("iris", 10)),
                rx.text("Scheduler", size="3"),
                align="center",
                width="100%",
                spacing="2",
            ),
            rx.tooltip(
                rx.box(
                    rx.select(
                        [
                            "DDIM",
                            "DPMSolverMultistep",
                            "HeunDiscrete",
                            "KarrasDPM",
                            "K_EULER_ANCESTRAL",
                            "K_EULER",
                            "PNDM",
                            "DPM++2MSDE",
                        ],
                        width="100%",
                        value=OptionsState.scheduler,
                        on_change=OptionsState.set_scheduler,
                    ),
                    width="100%",
                ),
                content="Schedulers guide the process of removing noise from the image",
                side="right",
            ),
            spacing="2",
        ),
    )


def _guidance_scale_input() -> rx.Component:
    return (
        rx.vstack(
            rx.hstack(
                rx.icon("scale", size=17, color=rx.color("cyan", 10)),
                rx.text("Guidance Scale", size="3"),
                rx.spacer(),
                rx.text(f"{OptionsState.guidance_scale}", size="3"),
                align="center",
                width="100%",
                spacing="2",
            ),
            rx.tooltip(
                rx.box(
                    rx.slider(
                        min=0,
                        max=50,
                        step=0.01,
                        size="1",
                        default_value=OptionsState.guidance_scale,
                        on_change=OptionsState.set_guidance_scale,
                    ),
                    width="100%",
                ),
                content="Controls the strength of the promptguidance. Recommended 0. (minimum: 0, maximum: 50)",
                side="right",
            ),
            spacing="2",
        ),
    )


def _steps_input() -> rx.Component:
    return (
        rx.vstack(
            rx.hstack(
                rx.icon("footprints", size=17, color=rx.color("purple", 10)),
                rx.text("Steps", size="3"),
                rx.spacer(),
                rx.text(f"{OptionsState.steps}", size="3"),
                align="center",
                width="100%",
                spacing="2",
            ),
            rx.tooltip(
                rx.box(
                    rx.slider(
                        min=1,
                        max=10,
                        step=1,
                        size="1",
                        default_value=OptionsState.steps,
                        on_change=OptionsState.set_steps,
                    ),
                    width="100%",
                ),
                content="Number of denoising steps. 4 for best results. (minimum: 1, maximum: 10)",
                side="right",
            ),
            spacing="2",
        ),
    )


def _advanced_options_grid() -> rx.Component:
    return rx.grid(
        _seed_input(),
        _steps_input(),
        _scheduler_input(),
        _guidance_scale_input(),
        width="100%",
        columns="2",
        rows="2",
        spacing_x="5",
        spacing_y="5",
        justify="between",
        align="center",
    )


def advanced_options() -> rx.Component:
    return rx.vstack(
        rx.cond(
            OptionsState.advanced_options_open,
            rx.hstack(
                rx.icon(
                    "eye",
                    size=17,
                    color=rx.color("jade", 10),
                ),
                rx.text("Advanced Options", size="3"),
                align="center",
                spacing="2",
                width="100%",
                cursor="pointer",
                _hover={"opacity": "0.8"},
                on_click=OptionsState.setvar("advanced_options_open", False),
            ),
            rx.hstack(
                rx.icon(
                    "eye-off",
                    size=17,
                    color=rx.color("jade", 10),
                ),
                rx.text("Advanced Options", size="3"),
                align="center",
                spacing="2",
                width="100%",
                cursor="pointer",
                _hover={"opacity": "0.8"},
                on_click=OptionsState.setvar("advanced_options_open", True),
            ),
        ),
        rx.cond(
            OptionsState.advanced_options_open,
            rx.vstack(_negative_prompt(), _advanced_options_grid(), width="100%"),
        ),
        width="100%",
    )


def generate_button() -> rx.Component:
    return rx.box(
        rx.cond(
            ~GeneratorState.is_generating,
            rx.button(
                rx.icon("sparkles", size=18),
                "Generate",
                size="3",
                cursor="pointer",
                width="100%",
                on_click=GeneratorState.generate_image,
            ),
            rx.button(
                rx.spinner(size="3"),
                "Cancel",
                size="3",
                width="100%",
                color_scheme="tomato",
                cursor="pointer",
                on_click=GeneratorState.cancel_generation,
            ),
        ),
        position="sticky",
        bottom="0",
        padding="1em",
        bg=rx.color("gray", 2),
        border_top=styles.border,
        width="100%",
    )
