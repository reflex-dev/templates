import reflex as rx

from space_dashboard.states.dashboard_state import DashboardState


def header() -> rx.Component:
    """The dashboard header."""
    return rx.el.header(
        rx.el.div(
            rx.el.span("// ", class_name="text-cyan-600"),
            rx.el.span(
                "ARES_DASHBOARD",
                class_name="text-white font-semibold tracking-wider",
            ),
            class_name="text-lg",
        ),
        rx.el.div(
            rx.el.span(
                DashboardState.user_status,
                class_name="text-gray-400 text-xs uppercase tracking-wider mr-2",
            ),
            rx.el.span(
                DashboardState.live_status,
                class_name="text-green-500 text-xs font-bold",
            ),
            class_name="flex items-center max-md:hidden",
        ),
        class_name="flex justify-between items-center w-full px-6 py-4 border-b border-blue-800/50",
    )
