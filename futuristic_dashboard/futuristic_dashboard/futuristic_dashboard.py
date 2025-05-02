import reflex as rx

from futuristic_dashboard.components.header import dashboard_header
from futuristic_dashboard.components.main_content import main_content
from futuristic_dashboard.components.right_sidebar import right_sidebar
from futuristic_dashboard.components.sidebar import sidebar
from futuristic_dashboard.states.dashboard_state import DashboardState


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            dashboard_header(),
            rx.el.div(
                main_content(),
                right_sidebar(),
                class_name="flex flex-1 overflow-hidden",
            ),
            class_name="flex flex-col flex-1 overflow-hidden",
        ),
        rx.cond(
            DashboardState.mobile_sidebar_open,
            rx.el.div(
                on_click=DashboardState.toggle_mobile_sidebar,
                class_name="fixed inset-0 bg-black/50 z-30 md:hidden",
            ),
            None,
        ),
        class_name="flex h-screen bg-gray-950 text-gray-300 relative",
        on_mount=DashboardState.update_time,
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/feather-icons/4.29.0/feather.min.js"
    ],
)
app.add_page(index)
