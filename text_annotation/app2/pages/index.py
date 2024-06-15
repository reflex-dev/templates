import reflex as rx


from app2.components.navbar import render_navbar
from app2.components.annotation import render_annotation_panel
from app2.components.document import render_document


@rx.page("/")
def index() -> rx.Component:
    return rx.vstack(
        render_navbar(),
        rx.hstack(
            render_annotation_panel(),
            render_document(),
            width="100%",
            display="flex",
            flex_wrap="wrap",
            spacing="6",
            padding="2em 1em",
        ),
        spacing="2",
    )
