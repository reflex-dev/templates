import reflex as rx

from space_dashboard.components.section_wrapper import section_wrapper
from space_dashboard.states.dashboard_state import (
    DashboardState,
    EnvData,
)


def environment_item(data: EnvData) -> rx.Component:
    """Displays a single environment metric."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    data["unit"],
                    class_name="text-xs text-cyan-400 font-bold",
                ),
                class_name="w-12 h-12 rounded-full border-2 border-cyan-600 flex items-center justify-center mr-4 bg-black/20",
            ),
            class_name="flex-shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                data["label"],
                class_name="text-xs text-cyan-400 uppercase",
            ),
            rx.el.p(
                data["value"],
                class_name="text-2xl text-white font-light tracking-wide",
            ),
            class_name="flex-grow",
        ),
        class_name="flex items-center mb-4",
    )


def environment_section() -> rx.Component:
    """The environment monitoring section."""
    return section_wrapper(
        "ENVIRONMENT",
        rx.foreach(
            DashboardState.environment_data,
            environment_item,
        ),
    )
