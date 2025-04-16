import reflex as rx
from admin_dashboard.components.navigation import navigation
from admin_dashboard.components.data_table import data_table
from admin_dashboard.components.customer_details import customer_details
from admin_dashboard.states.dashboard_state import DashboardState
from admin_dashboard.states.navigation_state import NavigationState


def index() -> rx.Component:
    """The main page layout for the dashboard."""
    return rx.el.div(
        navigation(),
        rx.el.div(
            rx.el.div(
                data_table(),
                class_name="flex-grow p-6 overflow-y-auto",
            ),
            customer_details(),
            class_name="flex flex-row h-[calc(100vh-56px)] overflow-hidden",
        ),
        class_name="bg-gray-100 h-screen overflow-hidden",
    )


def mock_page(title: str) -> rx.Component:
    """Creates a simple mock page layout."""
    return rx.el.div(
        navigation(),
        rx.el.div(
            rx.el.h1(
                title,
                class_name="text-2xl font-bold mb-4 text-gray-800",
            ),
            rx.el.p(
                f"Content for {title} goes here.",
                class_name="text-gray-600",
            ),
            class_name="p-6",
        ),
        class_name="bg-gray-100 h-screen",
    )


def sales_pipeline_page() -> rx.Component:
    """Mock Sales Pipeline page."""
    return mock_page("Sales Pipeline")


def hr_portal_page() -> rx.Component:
    """Mock HR Portal page."""
    return mock_page("HR Portal")


def customer_success_hub_page() -> rx.Component:
    """Mock Customer Success Hub page."""
    return mock_page("Customer Success Hub")


app = rx.App(
    theme=rx.theme(appearance="light"), stylesheets=[]
)
app.add_page(index, route="/")
app.add_page(sales_pipeline_page, route="/sales-pipeline")
app.add_page(hr_portal_page, route="/hr-portal")
app.add_page(
    customer_success_hub_page, route="/customer-success-hub"
)