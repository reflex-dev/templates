import reflex as rx

from .backend.backend import State
from .views.navbar import navbar
from .views.stats import stats_ui
from .views.table import main_table


def _tabs_trigger(text: str, icon: str, value: str):
    return rx.tabs.trigger(
        rx.hstack(
            rx.icon(icon, size=24),
            rx.heading(text, size="5"),
            spacing="2",
            align="center",
            width="100%",
        ),
        value=value,
    )


def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.tabs.root(
            rx.tabs.list(
                _tabs_trigger("Table", "table-2", value="table"),
                _tabs_trigger("Stats", "bar-chart-3", value="stats"),
            ),
            rx.tabs.content(
                main_table(),
                margin_top="1em",
                value="table",
            ),
            rx.tabs.content(
                stats_ui(),
                margin_top="1em",
                value="stats",
            ),
            default_value="table",
            width="100%",
        ),
        width="100%",
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em", "5em"],
        padding_y=["1.25em", "1.25em", "2em"],
    )


base_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
    "grid.css",
]

base_style = {
    "font_family": "Inter",
}

app = rx.App(
    style=base_style,
    stylesheets=base_stylesheets,
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="orange"
    ),
)
app.add_page(
    index,
    on_load=State.load_entries,
    title="NBA Data",
    description="NBA Data for the 2015-2016 season.",
)
