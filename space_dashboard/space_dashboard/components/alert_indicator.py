import reflex as rx

from space_dashboard.states.dashboard_state import DashboardState


def alert_indicator() -> rx.Component:
    """A flashing red alert indicator."""
    return rx.el.div(
        rx.el.div(
            DashboardState.alert_value.to_string(),
            class_name="text-white text-xs font-bold",
        ),
        class_name="absolute top-10 right-10 w-10 h-10 bg-red-600 rounded-full flex items-center justify-center border-2 border-red-400 shadow-lg animate-pulse",
    )
