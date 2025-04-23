import reflex as rx

from retail_analytics_dashboard.components.overview_chart import overview_chart
from retail_analytics_dashboard.states.dashboard_state import (
    DashboardState,
    OverviewMetric,
)


def customize_chart_item(
    metric: rx.Var[OverviewMetric],
) -> rx.Component:
    """Renders a single chart item with a checkbox in the customize dialog."""
    return rx.el.div(
        overview_chart(metric),
        rx.el.input(
            type="checkbox",
            checked=DashboardState.temp_chart_visibility[metric["id"]],
            on_click=lambda: DashboardState.toggle_temp_chart_visibility(metric["id"]),
            class_name="absolute top-3 right-3 h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded cursor-pointer",
        ),
        class_name="relative bg-white rounded-md shadow-sm border border-gray-200",
    )


def customize_charts_dialog() -> rx.Component:
    """Dialog to customize which overview charts are visible."""

    return rx.cond(
        DashboardState.show_customize_dialog,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity backdrop-blur-sm",
                on_click=DashboardState.cancel_chart_visibility,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Customise overview charts",
                        class_name="text-lg font-medium text-gray-900 mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(
                            DashboardState.overview_metrics,
                            customize_chart_item,
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=DashboardState.cancel_chart_visibility,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
                        ),
                        rx.el.button(
                            "Apply",
                            on_click=DashboardState.apply_chart_visibility,
                            class_name="ml-3 inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
                        ),
                        class_name="flex justify-end",
                    ),
                    class_name="p-6 bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[38rem] overflow-y-auto",
                ),
                class_name="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4",
            ),
            class_name="fixed inset-0 z-50 overflow-hidden",
        ),
        rx.el.div(),
    )
