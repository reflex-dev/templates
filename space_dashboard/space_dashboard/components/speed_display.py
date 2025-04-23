import reflex as rx

from space_dashboard.states.dashboard_state import DashboardState


def speed_display() -> rx.Component:
    """The central speed display."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        DashboardState.current_speed.to_string(),
                        class_name="text-6xl text-white font-thin tracking-tighter mb-1",
                    ),
                    rx.el.p(
                        "km/h",
                        class_name="text-xl text-cyan-400 uppercase tracking-widest",
                    ),
                    class_name="flex flex-col items-center justify-center text-center",
                ),
                class_name="w-64 h-64 rounded-full border-2 border-cyan-600/50 flex items-center justify-center bg-black/10 shadow-inner",
            ),
            class_name="w-80 h-80 rounded-full border border-cyan-700/40 p-2 flex items-center justify-center bg-black/10",
        ),
        class_name="w-96 h-96 rounded-full border border-blue-800/30 p-4 flex items-center justify-center bg-gradient-to-br from-blue-900/10 to-black/20 shadow-2xl relative",
    )
