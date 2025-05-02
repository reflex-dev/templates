import reflex as rx

from space_dashboard.components.alert_indicator import alert_indicator
from space_dashboard.components.control_buttons import control_buttons
from space_dashboard.components.data_stream import data_stream_section
from space_dashboard.components.environment import environment_section
from space_dashboard.components.header import header
from space_dashboard.components.hq_coms import hq_coms_section
from space_dashboard.components.planets import planets_section
from space_dashboard.components.pos_tracking import pos_tracking_section
from space_dashboard.components.speed_display import speed_display


def index() -> rx.Component:
    """The main dashboard page."""
    return rx.el.div(
        header(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    environment_section(),
                    planets_section(),
                    class_name="flex flex-col gap-6",
                ),
                rx.el.div(
                    rx.el.div(
                        speed_display(),
                        alert_indicator(),
                        control_buttons(),
                        class_name="flex flex-col items-center justify-center flex-grow relative",
                    ),
                    class_name="flex items-center justify-center",
                ),
                rx.el.div(
                    hq_coms_section(),
                    pos_tracking_section(),
                    data_stream_section(),
                    class_name="flex flex-col gap-6",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6 flex-grow",
            ),
            class_name="flex flex-col flex-grow",
        ),
        class_name="min-h-screen bg-gradient-to-br from-blue-950 via-black to-blue-950 text-cyan-200 flex flex-col",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)
