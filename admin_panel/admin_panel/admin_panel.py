import reflex as rx

from admin_panel.components.customer_form import customer_edit_form
from admin_panel.components.customer_table import customer_table
from admin_panel.states.customer_state import CustomerState


def index() -> rx.Component:
    return rx.el.div(
        rx.el.main(
            rx.el.div(
                rx.cond(
                    CustomerState.error_message != "",
                    rx.el.div(
                        CustomerState.error_message,
                        class_name=rx.cond(
                            CustomerState.error_message.contains("Failed")
                            | CustomerState.error_message.contains(
                                "Failed to simulate"
                            ),
                            "mb-4 p-4 rounded-md text-sm bg-red-100 border border-red-300 text-red-700 shadow",
                            "mb-4 p-4 rounded-md text-sm bg-yellow-100 border border-yellow-300 text-yellow-700 shadow",
                        ),
                    ),
                    rx.fragment(),
                ),
                customer_table(),
                customer_edit_form(),
                class_name="mx-auto w-full lg:p-8 p-4",
            )
        ),
        class_name="min-h-screen bg-gray-100 font-['Inter']",
    )


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
app.add_page(index, route="/", on_load=CustomerState.fetch_customers)
