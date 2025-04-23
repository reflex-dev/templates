import reflex as rx

from manufacturing_dashboard.states.dashboard_state import DashboardState


def dashboard_header() -> rx.Component:
    """Renders the header section of the dashboard."""
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "CONTROL CHARTS DASHBOARD",
                class_name="text-xs font-semibold text-slate-400 tracking-wider uppercase mr-4",
            ),
            rx.el.button(
                rx.cond(
                    DashboardState.is_running,
                    "Running...",
                    "Start Process",
                ),
                on_click=DashboardState.start_process,
                disabled=DashboardState.is_running,
                class_name=rx.cond(
                    DashboardState.is_running,
                    "px-4 py-1.5 text-sm font-medium text-slate-300 bg-slate-700 rounded-md opacity-50 cursor-not-allowed",
                    "px-4 py-1.5 text-sm font-medium text-white bg-cyan-600 rounded-md hover:bg-cyan-700 transition-colors duration-150",
                ),
            ),
            class_name="flex flex-1 justify-between items-center border-b-2 border-cyan-600 pb-2",
        ),
        class_name="flex justify-between items-center mb-8",
    )
