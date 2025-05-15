import reflex as rx

from stock_graph_app.components.stock_chart_display import (
    stock_graph_page,
)


def index() -> rx.Component:
    return rx.el.div(
        stock_graph_page(),
        class_name="min-h-screen bg-[#202123] flex items-center justify-center p-4 font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            rel="preconnect",
            href="https://fonts.googleapis.com",
        ),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            crossorigin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400..700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)
