import reflex as rx
from . import styles

# Import all the pages.
from .pages import *

app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
    html_lang="en",
    html_custom_attrs={"className": "!scroll-smooth"},
    theme=rx.theme(
        appearance="inherit",
        has_background=True,
        scaling="100%",
        radius="none",
        accent_color="violet",
    ),
)
