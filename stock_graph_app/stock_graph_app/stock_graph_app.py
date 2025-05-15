import reflex as rx
from stock_graph_app.components.stock_chart_display import (
    stock_graph_page,
)


def index() -> rx.Component:
    return rx.el.div(
        stock_graph_page(),
        class_name="min-h-screen bg-[#202123] flex items-center justify-center p-4",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)
