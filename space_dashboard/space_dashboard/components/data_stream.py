import reflex as rx

from space_dashboard.components.section_wrapper import section_wrapper
from space_dashboard.states.dashboard_state import (
    DashboardState,
    StreamData,
)


def data_stream_item(data: StreamData) -> rx.Component:
    """Displays a single data stream item."""
    return rx.el.div(
        rx.el.p(
            data["label"],
            class_name="text-sm text-cyan-400 uppercase font-semibold",
        ),
        rx.el.p(
            data["value"].to_string(),
            class_name="text-lg text-white font-mono",
        ),
        class_name="text-center p-2",
    )


def data_stream_section() -> rx.Component:
    """The Data Stream section."""
    return section_wrapper(
        "DATA_STREAM",
        rx.el.div(
            rx.foreach(
                DashboardState.data_stream_data,
                data_stream_item,
            ),
            class_name="grid grid-cols-3 gap-2",
        ),
    )
