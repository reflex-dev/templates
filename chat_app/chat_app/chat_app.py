import reflex as rx

from chat_app.components.chat_interface import chat_interface


def index() -> rx.Component:
    """The main page of the chat application."""
    return chat_interface()


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)
