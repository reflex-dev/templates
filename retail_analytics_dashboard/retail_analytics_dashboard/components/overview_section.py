import reflex as rx

from retail_analytics_dashboard.components.overview_chart import overview_chart
from retail_analytics_dashboard.states.dashboard_state import DashboardState


def overview_section() -> rx.Component:
    """The overview section with metric charts."""
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Overview",
                class_name="text-xl font-semibold text-gray-800",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        tag="settings",
                        class_name="w-4 h-4 mr-2",
                    ),
                    "Edit",
                    on_click=DashboardState.toggle_customize_dialog,
                    class_name="ml-auto flex items-center px-3 py-1.5 border border-gray-300 bg-white rounded-md text-sm text-gray-700 hover:bg-gray-50 shadow-sm",
                ),
                class_name="flex items-center space-x-2",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.foreach(
                DashboardState.visible_overview_metrics,
                overview_chart,
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
    )
