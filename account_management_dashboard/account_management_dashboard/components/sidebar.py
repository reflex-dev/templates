import reflex as rx

from account_management_dashboard.states.account_state import AccountState


def sidebar_item(item: dict[str, str]) -> rx.Component:
    """Component for a single item in the sidebar."""
    is_active = AccountState.active_page == item["name"]
    return rx.el.a(
        rx.el.div(
            rx.icon(tag=item["icon"], class_name="w-5 h-5 mr-3"),
            rx.el.span(item["name"]),
            class_name=rx.cond(
                is_active,
                "flex items-center px-4 py-2.5 text-sm font-semibold text-gray-900 bg-gray-100 rounded-lg",
                "flex items-center px-4 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50 rounded-lg transition-colors duration-150 cursor-pointer",
            ),
        ),
        on_click=lambda: AccountState.set_active_page(item["name"]),
        href="#",
    )


def sidebar() -> rx.Component:
    """The sidebar component for navigation."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Account Management", class_name="text-md font-bold"),
            class_name="p-4",
        ),
        rx.el.nav(
            rx.el.div(
                rx.foreach(AccountState.sidebar_items, sidebar_item),
                class_name="space-y-1",
            ),
            class_name="flex-grow px-4 overflow-y-auto",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon(
                        tag="circle_plus",
                        class_name="w-5 h-5 mr-3",
                    ),
                    rx.el.span("Help & Support"),
                    href="#",
                    class_name="flex items-center px-4 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50 rounded-lg transition-colors duration-150",
                ),
                class_name="mb-2 pt-4 border-t border-gray-200",
            ),
            rx.el.div(
                rx.el.button(
                    rx.el.div(
                        rx.el.div(
                            AccountState.user_name[0],
                            class_name="w-8 h-8 rounded-full bg-gray-300 text-gray-700 flex items-center justify-center font-semibold text-sm mr-3",
                        )
                    ),
                    rx.el.span(
                        AccountState.user_name,
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.icon(
                        tag="chevron_down",
                        class_name="w-4 h-4 ml-auto text-gray-500",
                    ),
                    class_name="flex items-center w-full px-4 py-3 text-left hover:bg-gray-50 rounded-lg transition-colors duration-150",
                )
            ),
            class_name="px-4 pb-4",
        ),
        class_name="flex flex-col w-full max-w-[250px] h-screen bg-white border-r border-gray-200 sticky left-0 top-0 max-lg:hidden",
    )
