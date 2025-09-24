"""Main entry point for the combined enterprise demos."""

import reflex as rx
import reflex_enterprise as rxe

from .demo import enterprise_sidebar


@rx.page(route="/")
def index() -> rx.Component:
    """The index page for the enterprise demos."""
    return rx.box(
        enterprise_sidebar(),
        rx.box(
            rx.vstack(
                rx.heading("Welcome to the Enterprise Demos!"),
                rx.text("Select a demo from the sidebar to get started."),
                align="center",
            ),
            padding="1em",
            margin_left="260px",
            width="calc(100% - 260px)",
            height="100%",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        height="100vh",
    )


# Create the app.
app = rxe.App()
