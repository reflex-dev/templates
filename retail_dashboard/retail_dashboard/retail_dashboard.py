from typing import Callable

import reflex as rx

from retail_dashboard.components.sidebar import sidebar
from retail_dashboard.pages.details_page import details_page_layout
from retail_dashboard.states.dashboard_state import DashboardState


def page_with_sidebar(
    content_func: Callable[[], rx.Component],
) -> rx.Component:
    """Main page layout with sidebar and content area."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            content_func(),
            class_name="flex-1 overflow-y-auto bg-gray-50 p-0",
        ),
        rx.el.div(
            class_name=rx.cond(
                DashboardState.show_status_filter
                | DashboardState.show_country_filter
                | DashboardState.show_costs_filter,
                "fixed inset-0 bg-black bg-opacity-20 z-20",
                "hidden",
            ),
            on_click=DashboardState.close_filter_dropdowns,
        ),
        class_name="flex h-screen font-['Inter']",
    )


def details_route() -> rx.Component:
    """Route for the Details page."""
    return page_with_sidebar(details_page_layout)


def index() -> rx.Component:
    """Default route, now pointing to details page."""
    return details_route()


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            rel="preconnect",
            href="https://fonts.googleapis.com",
        ),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            crossorigin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400..700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
