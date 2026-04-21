"""Shared components for demos."""

import dataclasses
import inspect
from functools import wraps
from pathlib import Path
from typing import Callable

import reflex as rx


def enterprise_sidebar():
    return rx.box(
        rx.box(
            "Enterprise Demos",
            class_name="w-full h-10 absolute top-0 left-0 flex items-center px-3 font-semibold",
        ),
        rx.box(
            rx.vstack(
                rx.link("AG Grid", href="/ag-grid"),
                rx.link("Drag and Drop", href="/dnd"),
                rx.link("Flow", href="/flow"),
                rx.link("Mantine", href="/mantine"),
                rx.link("Map", href="/map"),
                spacing="2",
                align_items="start",
                width="100%",
            ),
            class_name="flex flex-col",
            width="260px",
        ),
        bg=rx.color("gray", 2),
        class_name="flex flex-col pt-12 px-3",
        width="260px",
        height="100vh",
        overflow_y="auto",
        position="fixed",
        top="0",
        left="0",
    )


@dataclasses.dataclass(frozen=True)
class DemoPage:
    """A demo page."""

    route: str
    title: str
    description: str


def demo_builder(demo_prefix: str, demo_title: str):
    """Factory for demo components."""
    _DEMO_PAGES: dict[str, DemoPage] = {}

    class DemoState(rx.State):
        """State for the demo pages."""

        @rx.var
        def pages(self) -> list[DemoPage]:
            """List of demo pages."""
            return sorted(
                [p for p in _DEMO_PAGES.values() if p.route != demo_prefix],
                key=lambda p: p.title,
            )

    def demo_dropdown():
        """Dropdown to navigate between demo pages."""
        return rx.select.root(
            rx.select.trigger(placeholder="Select Demo"),
            rx.select.content(
                rx.foreach(
                    DemoState.pages,
                    lambda page: rx.select.item(
                        rx.heading(page.title, size="3"), value=page.route
                    ),
                )
            ),
            value=rx.cond(
                rx.State.router.page.path == demo_prefix,
                "",
                rx.State.router.page.path,
            ),
            on_change=rx.redirect,
        )

    def demo_template(page: Callable):
        """Template for all demo pages."""
        page_data = _DEMO_PAGES[page.__name__]
        page_file = Path(inspect.getfile(page))
        page_source = page_file.read_text()
        relative_page_file = page_file.relative_to(
            Path(__file__).parent.parent.parent.resolve()
        )

        page_content = rx.container(
            rx.hstack(
                demo_dropdown(),
                rx.spacer(),
                rx.link(
                    rx.heading(demo_title, size="4"),
                    href=demo_prefix,
                ),
                rx.color_mode.button(),
                width="100%",
                align="center",
            ),
            rx.text(page_data.description, margin_left="10px", margin_top="5px"),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(
                        rx.hstack(rx.icon("eye"), rx.text("Example")), value="example"
                    ),
                    rx.tabs.trigger(
                        rx.hstack(rx.icon("code"), rx.text("Source")), value="source"
                    ),
                    margin_bottom="1em",
                ),
                rx.tabs.content(page(), value="example", height="fit-content"),
                rx.tabs.content(
                    rx.card(
                        rx.inset(
                            rx.badge(
                                rx.code(str(relative_page_file)),
                                width="100%",
                                size="2",
                                height="3em",
                                radius="none",
                            ),
                            side="top",
                            pb="current",
                        ),
                        rx.code_block(
                            page_source, language="python", show_line_numbers=True
                        ),
                    ),
                    value="source",
                ),
                default_value="example",
                margin_top="1em",
            ),
            size="4",
        )

        return rx.box(
            enterprise_sidebar(),
            rx.box(
                page_content,
                padding="1em",
                margin_left="260px",
                width="calc(100% - 260px)",
            ),
            height="100vh",
        )

    def demo(route: str, title: str, description: str, **kwargs):
        """Decorator to add the demo page to the demo registry."""

        def decorator(page: Callable):
            new_route = f"{demo_prefix}{route if route != '/' else ''}"
            _DEMO_PAGES[page.__name__] = DemoPage(
                route=new_route, title=title, description=description
            )

            @rx.page(route=new_route, title=title, description=description, **kwargs)
            @wraps(page)
            def inner():
                return demo_template(page)

            return inner

        return decorator

    return demo, DemoState
