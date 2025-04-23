import reflex as rx

from space_dashboard.components.section_wrapper import section_wrapper
from space_dashboard.states.dashboard_state import (
    DashboardState,
    PosData,
)


def pos_tracking_item(data: PosData) -> rx.Component:
    """Displays a single position tracking metric with a progress bar."""
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                f"{data['label']}:",
                class_name="text-sm text-cyan-400 mr-2 font-semibold",
            ),
            rx.el.span(
                data["value"].to_string(),
                class_name="text-sm text-white font-mono",
            ),
            class_name="flex justify-between items-center mb-1",
        ),
        rx.el.progress(
            value=data["value"],
            max=100,
            class_name="w-full h-1.5 bg-blue-900/50 rounded-full overflow-hidden",
        ),
        class_name="mb-3",
    )


def pos_tracking_section() -> rx.Component:
    """The Position Tracking section."""
    return section_wrapper(
        "POS_TRACKING",
        rx.foreach(
            DashboardState.pos_tracking_data,
            pos_tracking_item,
        ),
    )
