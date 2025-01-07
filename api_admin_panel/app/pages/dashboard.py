"""The dashboard page."""

import reflex as rx

from app.components.navbar import render_navbar
from app.components.output import render_output
from app.components.query import render_query_component
from app.states.queries import QueryAPI


@rx.page("/", on_load=QueryAPI.run_get_request)
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.

    """
    return rx.vstack(
        render_navbar(),
        rx.hstack(
            render_query_component(),
            render_output(),
            width="100%",
            display="flex",
            flex_wrap="wrap",
            spacing="6",
            padding="2em 1em",
        ),
        spacing="4",
    )
