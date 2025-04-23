import reflex as rx

from space_dashboard.components.section_wrapper import section_wrapper
from space_dashboard.states.dashboard_state import (
    DashboardState,
    PlanetData,
)


def planet_item(data: PlanetData) -> rx.Component:
    """Displays a single planet distance."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name=f"w-8 h-8 rounded-full {data['color']} mr-4 border-2 border-white/50"
            ),
            class_name="flex-shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                data["name"],
                class_name="text-sm text-cyan-400 uppercase font-semibold",
            ),
            rx.el.p(
                data["distance"],
                class_name="text-xl text-white font-light tracking-wide",
            ),
            class_name="flex-grow",
        ),
        class_name="flex items-center mb-3",
    )


def planets_section() -> rx.Component:
    """The planets distance section."""
    return section_wrapper(
        "PLANETS",
        rx.foreach(DashboardState.planets_data, planet_item),
    )
