import reflex as rx

from manufacturing_dashboard.components.dashboard_header import dashboard_header
from manufacturing_dashboard.components.metrics_summary import metrics_summary
from manufacturing_dashboard.components.pie_chart import ooc_pie_chart
from manufacturing_dashboard.components.sidebar import sidebar
from manufacturing_dashboard.components.spc_chart import spc_chart


def index() -> rx.Component:
    """The main dashboard page."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            dashboard_header(),
            metrics_summary(),
            spc_chart(),
            rx.el.div(
                ooc_pie_chart(),
                class_name="mt-6 grid grid-cols-1 gap-6",
            ),
            class_name="w-full p-8 overflow-y-auto bg-slate-900 text-slate-100 min-h-screen lg:ml-64",
        ),
        class_name="flex max-h-screen w-full",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    style={
        "font_family": "'Inter', sans-serif",
        "height": "100%",
        "background_color": "#0f172a",
        "::selection": {
            "background_color": "#06b6d4",
            "color": "#ffffff",
        },
        "body": {"height": "100%", "margin": 0},
        "#__next": {"height": "100%"},
    },
)
app.add_page(index)
