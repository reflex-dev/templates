import reflex as rx

from retail_analytics_dashboard.components.progress_bar import (
    cost_progress_bar,
    progress_bar,
)
from retail_analytics_dashboard.states.dashboard_state import DashboardState


def billing_cycle_stats() -> rx.Component:
    """Renders billing cycle stats."""
    return rx.el.div(
        rx.foreach(
            DashboardState.billing_usage_stats,
            lambda item: progress_bar(
                label=item["label"],
                value=item["value"],
                total=item["total"],
                percentage=item["percentage"],
            ),
        ),
        class_name="space-y-4",
    )


def billing_workspace_stats() -> rx.Component:
    """Renders billing workspace stats."""
    return rx.el.div(
        rx.foreach(
            DashboardState.billing_workspace_stats,
            lambda item: progress_bar(
                label=item["label"],
                value=item["value"],
                total=item["total"],
                percentage=item["percentage"],
            ),
        ),
        class_name="space-y-4",
    )


def billing_costs() -> rx.Component:
    """Renders billing costs."""
    return cost_progress_bar(items=DashboardState.billing_costs_items)


def billing_cycle() -> rx.Component:
    """The billing cycle section with usage stats, workspace stats and cost breakdown."""
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Billing Cycle",
                class_name="text-xl font-semibold text-gray-800",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        tag="calendar",
                        class_name="w-4 h-4 mr-2",
                    ),
                    "16 Apr, 2024 - 16 May, 2024",
                    class_name="flex items-center px-3 py-1.5 border border-gray-300 rounded-md text-sm text-gray-700 hover:bg-gray-50",
                ),
                rx.el.button(
                    rx.icon(
                        tag="chevron_down",
                        class_name="w-4 h-4 ml-2",
                    ),
                    class_name="text-gray-400 hover:text-gray-600 focus:outline-none",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Usage stats",
                    class_name="text-lg font-semibold text-gray-700 mb-4",
                ),
                billing_cycle_stats(),
                class_name="bg-white p-6 rounded-md shadow-sm",
            ),
            rx.el.div(
                rx.el.h3(
                    "Workspace stats",
                    class_name="text-lg font-semibold text-gray-700 mb-4",
                ),
                billing_workspace_stats(),
                class_name="bg-white p-6 rounded-md shadow-sm",
            ),
            rx.el.div(
                rx.el.h3(
                    "Cost breakdown",
                    class_name="text-lg font-semibold text-gray-700 mb-4",
                ),
                billing_costs(),
                class_name="bg-white p-6 rounded-md shadow-sm",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
    )
