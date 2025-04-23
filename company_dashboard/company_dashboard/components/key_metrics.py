import reflex as rx

from company_dashboard.states.dashboard_state import (
    DashboardState,
    Metric,
)


def metric_card(metric: Metric) -> rx.Component:
    """A card displaying a single key metric."""
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                metric["title"],
                class_name="text-sm font-medium text-gray-500",
            ),
            rx.el.div(
                rx.el.span(
                    metric["change"],
                    class_name=rx.cond(
                        metric["change_direction"] == "up",
                        "text-xs font-medium px-2 py-0.5 rounded-full bg-green-100 text-green-800",
                        rx.cond(
                            metric["change_direction"] == "down",
                            "text-xs font-medium px-2 py-0.5 rounded-full bg-red-100 text-red-800",
                            "text-xs font-medium px-2 py-0.5 rounded-full bg-gray-100 text-gray-800",
                        ),
                    ),
                ),
                rx.icon(
                    tag=rx.cond(
                        metric["change_direction"] == "up",
                        "trending-up",
                        rx.cond(
                            metric["change_direction"] == "down",
                            "trending-down",
                            "minus",
                        ),
                    ),
                    size=16,
                    class_name=rx.cond(
                        metric["change_direction"] == "up",
                        "text-green-600 ml-1",
                        rx.cond(
                            metric["change_direction"] == "down",
                            "text-red-600 ml-1",
                            "text-gray-600 ml-1",
                        ),
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between mb-1",
        ),
        rx.el.p(
            metric["value"],
            class_name="text-3xl font-semibold text-gray-900 mb-2",
        ),
        rx.el.div(
            rx.el.p(
                metric["description"],
                class_name="text-sm text-gray-700 mr-1",
            ),
            rx.icon(
                tag="bar-chart-2",
                size=16,
                class_name="text-gray-500",
            ),
            class_name="flex items-center text-sm text-gray-500",
        ),
        rx.el.p(
            metric["trend_description"],
            class_name="text-xs text-gray-400 mt-1",
        ),
        class_name="p-5 bg-white border border-gray-200 rounded-lg shadow-sm",
    )


def key_metrics_section() -> rx.Component:
    """The section displaying key metric cards."""
    return rx.el.div(
        rx.foreach(DashboardState.key_metrics, metric_card),
        class_name="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4",
    )
