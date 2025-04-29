import reflex as rx

from company_dashboard.components.documents_table import (
    documents_table_section,
)
from company_dashboard.components.header import header_bar
from company_dashboard.components.key_metrics import key_metrics_section
from company_dashboard.components.sidebar import sidebar
from company_dashboard.components.visitors_chart import (
    visitors_chart_section,
)
from company_dashboard.states.dashboard_state import DashboardState


def index() -> rx.Component:
    """The main dashboard page."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header_bar(),
            rx.el.div(
                key_metrics_section(),
                visitors_chart_section(),
                documents_table_section(),
                class_name="p-6 space-y-6",
            ),
            class_name="w-full h-[100vh] overflow-y-auto",
        ),
        class_name="flex flex-row bg-gray-50 h-[100vh] w-full overflow-hidden",
        on_mount=DashboardState.load_initial_data,
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["https://cdn.tailwindcss.com"],
    style={
        rx.el.label: {"font_family": "JetBrains Mono,ui-monospace,monospace"},
        rx.el.span: {"font_family": "JetBrains Mono,ui-monospace,monospace"},
        rx.el.h1: {"font_family": "JetBrains Mono,ui-monospace,monospace"},
        rx.el.h2: {"font_family": "JetBrains Mono,ui-monospace,monospace"},
    },
)
app.add_page(index, route="/")
