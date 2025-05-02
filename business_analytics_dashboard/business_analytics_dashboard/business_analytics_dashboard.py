"""Basic Dashboard App"""

import reflex as rx

from business_analytics_dashboard.components.account_executive_metrics import (
    account_executive_metrics_table,
)
from business_analytics_dashboard.components.average_salary_chart import (
    average_salary_bar_chart,
)
from business_analytics_dashboard.components.department_pie_chart import (
    department_pie_chart,
)
from business_analytics_dashboard.components.sidebar import sidebar
from business_analytics_dashboard.states.dashboard_state import DashboardState


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
                department_pie_chart(),
                average_salary_bar_chart(),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6",
            ),
            account_executive_metrics_table(),
            class_name="p-4 bg-gray-100 h-[100vh] w-full overflow-y-auto",
            on_mount=DashboardState.fetch_dashboard_data,
        ),
        class_name="flex w-full min-h-screen",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)
