import reflex as rx

from retail_analytics_dashboard.components.billing_cycle import billing_cycle
from retail_analytics_dashboard.components.customize_charts_dialog import (
    customize_charts_dialog,
)
from retail_analytics_dashboard.components.overview_section import overview_section
from retail_analytics_dashboard.components.sidebar import sidebar


def index() -> rx.Component:
    """The main dashboard page."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            billing_cycle(),
            rx.el.div(class_name="mt-6"),
            overview_section(),
            class_name="flex-1 p-6 bg-gray-50 overflow-y-auto",
        ),
        customize_charts_dialog(),
        class_name="flex min-h-screen relative",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)
