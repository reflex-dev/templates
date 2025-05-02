import reflex as rx

from account_management_dashboard.states.account_state import AccountState


def header_component() -> rx.Component:
    """The header component above the main content area."""
    return rx.el.div(
        rx.el.h1(
            "Accounts",
            class_name="text-2xl font-semibold text-gray-900",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon(
                    tag="refresh_cw",
                    class_name="w-4 h-4 mr-2",
                ),
                "Refresh all",
                on_click=AccountState.refresh_all,
                class_name="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition",
            ),
            rx.el.button(
                rx.icon(tag="plus", class_name="w-4 h-4 mr-2"),
                "Add account",
                on_click=AccountState.add_account,
                class_name="flex items-center px-4 py-2 text-sm font-medium text-white bg-orange-500 border border-transparent rounded-md shadow-sm hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 transition",
            ),
            class_name="flex items-center space-x-3 max-md:hidden",
        ),
        class_name="w-full flex items-center justify-between pb-6 border-b border-gray-200 mb-6",
    )
