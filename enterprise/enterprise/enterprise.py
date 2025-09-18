"""Main entry point for the combined enterprise demos."""

import reflex as rx
import reflex_enterprise as rxe

# Import all the demo pages to register them.
from .ag_grid.ag_grid import ag_grid
from .dnd.dnd import dnd
from .flow.flow import flow
from .mantine.mantine import mantine
from .map.map import map


class State(rx.State):
    """The app state."""


def sidebar():
    return rx.vstack(
        rx.link("Home", href="/"),
        rx.divider(),
        rx.heading("Demos", size="4"),
        rx.link("AG Grid", href="/ag-grid"),
        rx.link("Drag and Drop", href="/dnd"),
        rx.link("Flow", href="/flow"),
        rx.link("Mantine", href="/mantine"),
        rx.link("Map", href="/map"),
        spacing="5",
        padding="1em",
        height="100%",
        border_right="1px solid #ddd",
        position="fixed",
        top="0",
        left="0",
        width="200px",
        background_color=rx.color("gray", 2),
    )


@rx.page(route="/")
def index() -> rx.Component:
    return rx.box(
        sidebar(),
        rx.box(
            rx.heading("Welcome to the Enterprise Demos!"),
            rx.text("Select a demo from the sidebar to get started."),
            padding="1em",
            margin_left="200px",
        ),
    )


# Create the app.
app = rxe.App()
