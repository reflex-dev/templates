import reflex as rx

from . import styles

# Import all the pages.
from .pages import *

app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
    html_lang="en",
    html_custom_attrs={"className": "!scroll-smooth"},
)
