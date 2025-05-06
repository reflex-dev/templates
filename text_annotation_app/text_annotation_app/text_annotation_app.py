import reflex as rx

from text_annotation_app.components.ner_display import ner_component
from text_annotation_app.states.ner_state import NerState


def index() -> rx.Component:
    """The main page of the app."""
    return rx.el.div(
        ner_component(),
        on_mount=NerState.process_text_on_load,
        class_name="min-h-screen bg-gray-50 p-4",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index, route="/")
