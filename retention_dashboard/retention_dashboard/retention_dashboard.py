import reflex as rx

from retention_dashboard.components.layout import layout


def index() -> rx.Component:
    """The main page of the app."""
    return layout()


app = rx.App()
app.add_page(index, route="/")
