"""AG Grid Demo."""

import reflex as rx

from .common import DemoState, demo
from .dates import dates_page
from .pill_demo import pill_page
from .tags_input import tags_input_page

__all__ = [
    "dates_page",
    "pill_page",
    "tags_input_page",
]


@demo(
    route="/",
    title="Mantine Demo",
    description="A collection of examples using Mantine in Reflex.",
)
def index():
    """Index page for the AG Grid demos."""
    return rx.flex(
        rx.foreach(
            DemoState.pages,
            lambda page: rx.card(
                rx.vstack(
                    rx.link(page.title, href=page.route),
                    rx.text(page.description),
                ),
                width="300px",
            ),
        ),
        wrap="wrap",
        spacing="3",
    )
