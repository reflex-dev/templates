"""Basic Dashboard App"""

import reflex as rx

from business_analytics_dashboard.components.account_executive_metrics import (
    account_executive_metrics_table,
)
from business_analytics_dashboard.components.department_pie_chart import (
    department_pie_chart,
)
from business_analytics_dashboard.components.sidebar import sidebar
from business_analytics_dashboard.states.dashboard_state import DashboardState


def expense_analysis_component() -> rx.Component:
    """Component displaying expense analysis data."""
    return rx.el.div(
        rx.el.h2(
            "Expense Analysis",
            class_name="text-2xl font-semibold text-gray-800 mb-4",
        ),
        rx.cond(
            DashboardState.loading_revenue,
            rx.el.p(
                "Loading expense data...",
                class_name="text-gray-600",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Total Reported Expenses:",
                        class_name="text-lg text-gray-700 font-medium",
                    ),
                    rx.el.p(
                        "$ " + DashboardState.formatted_total_expense,
                        class_name="text-3xl font-bold text-blue-600",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "Average Expense Report Amount:",
                        class_name="text-lg text-gray-700 font-medium",
                    ),
                    rx.el.p(
                        "$ " + DashboardState.formatted_average_expense,
                        class_name="text-2xl font-semibold text-green-600",
                    ),
                ),
                class_name="mt-2",
            ),
        ),
        class_name="bg-white p-6 rounded-lg h-auto min-h-[12rem]",
    )


def index() -> rx.Component:
    """The main dashboard page."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.h1(
                "Business Analytics Dashboard",
                class_name="text-3xl font-bold text-gray-800 mb-6",
            ),
            rx.el.div(
                expense_analysis_component(),
                department_pie_chart(),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6",
            ),
            account_executive_metrics_table(),
            class_name="ml-64 p-8 bg-gray-100 min-h-screen w-full",
            on_mount=DashboardState.fetch_dashboard_data,
        ),
        class_name="flex w-full",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)
