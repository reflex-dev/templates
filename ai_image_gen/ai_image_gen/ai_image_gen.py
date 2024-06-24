import reflex as rx

# Import all the pages.
from .pages import *

base_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Roboto+Flex:wght@400;500;600;700;800&display=swap",
    "react-zoom.css",
]

base_style = {
    "font_family": "Roboto Flex",
    rx.icon: {
        "stroke_width": "1.75px",
    },
}

app = rx.App(
    style=base_style,
    stylesheets=base_stylesheets,
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
