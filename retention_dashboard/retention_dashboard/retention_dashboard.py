import reflex as rx

from retention_dashboard.components.layout import layout


def index() -> rx.Component:
    """The main page of the app."""
    return layout()


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index, route="/")
