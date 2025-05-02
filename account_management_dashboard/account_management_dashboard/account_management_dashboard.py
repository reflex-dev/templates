import reflex as rx

from account_management_dashboard.components.account_section import (
    account_category_section,
)
from account_management_dashboard.components.header import header_component
from account_management_dashboard.components.net_worth_graph import (
    net_worth_graph_component,
)
from account_management_dashboard.components.net_worth_summary import (
    net_worth_summary,
)
from account_management_dashboard.components.sidebar import sidebar
from account_management_dashboard.components.summary_section import summary_section
from account_management_dashboard.states.account_state import AccountState


def index() -> rx.Component:
    """The main page of the financial dashboard."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header_component(),
            net_worth_summary(),
            net_worth_graph_component(),
            rx.el.div(
                rx.el.div(
                    rx.foreach(
                        AccountState.account_categories,
                        account_category_section,
                    ),
                    class_name="flex-grow pr-0 lg:pr-8 mb-8 lg:mb-0",
                ),
                rx.el.div(
                    summary_section(),
                    class_name="w-full lg:w-80 flex-shrink-0",
                ),
                class_name="flex flex-col lg:flex-row",
            ),
            rx.toast.provider(),
            class_name="p-8 flex flex-col w-full min-h-[100vh] overflow-y-auto",
        ),
        class_name="flex flex-row bg-gray-50 min-h-screen w-full",
    )


app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=False,
        radius="medium",
        accent_color="indigo",
    )
)
app.add_page(index, title="Accounts Dashboard")
