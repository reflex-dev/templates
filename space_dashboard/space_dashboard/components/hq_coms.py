import reflex as rx

from space_dashboard.components.section_wrapper import section_wrapper
from space_dashboard.states.dashboard_state import (
    ComData,
    DashboardState,
)


def hq_com_item(data: ComData) -> rx.Component:
    """Displays a single HQ Coms channel."""
    return rx.el.div(
        rx.el.p(
            f"{data['channel']} [{data['value'].to_string()}]",
            class_name="text-sm text-cyan-300 font-mono",
        ),
        class_name="p-1",
    )


def hq_coms_section() -> rx.Component:
    """The HQ Communications section."""
    return section_wrapper(
        "HQ_COMS",
        rx.el.div(
            rx.foreach(DashboardState.hq_coms_data, hq_com_item),
            class_name="grid grid-cols-2 gap-x-4 gap-y-1",
        ),
    )
