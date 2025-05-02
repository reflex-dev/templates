import reflex as rx

from space_dashboard.states.dashboard_state import DashboardState


def control_buttons() -> rx.Component:
    """The bottom center control buttons."""
    return rx.el.div(
        rx.foreach(
            DashboardState.control_buttons,
            lambda button_text: rx.el.button(
                button_text,
                class_name="flex-1 bg-gradient-to-br from-blue-900/50 to-black/40 border border-cyan-700/50 rounded text-cyan-300 text-sm uppercase tracking-wider py-3 px-4 hover:bg-cyan-900/50 hover:border-cyan-500 transition-all duration-200 font-semibold",
            ),
        ),
        class_name="grid grid-cols-2 gap-3 mt-8 w-full px-4 sm:px-0",
    )
