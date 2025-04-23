import reflex as rx

from table_dashboard.components.details_table import details_table
from table_dashboard.components.header import header
from table_dashboard.components.sidebar import sidebar
from table_dashboard.states.dashboard_state import DashboardState


def index() -> rx.Component:
    """The main dashboard page."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                header(),
                details_table(),
                class_name="p-6 space-y-6",
            ),
            class_name="flex-1 overflow-y-auto",
        ),
        rx.el.div(
            class_name=rx.cond(
                DashboardState.show_status_filter
                | DashboardState.show_region_filter
                | DashboardState.show_costs_filter,
                "fixed inset-0 z-5",
                "hidden",
            ),
            on_click=DashboardState.close_filter_dropdowns,
        ),
        class_name="flex h-screen",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)
