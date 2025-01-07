"""The dashboard page."""

import reflex as rx

from ..backend.table_state import TableState
from ..templates import template
from ..views.table import main_table


@template(route="/", title="Dashboard", on_load=TableState.load_entries)
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.

    """
    return rx.vstack(
        rx.heading("CI Job Dashboard", size="5"),
        main_table(),
        spacing="8",
        width="100%",
    )
