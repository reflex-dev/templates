import reflex as rx

from admin_panel.states.customer_state import CustomerData, CustomerState


def sortable_table_header_cell(text: str, column_key: str) -> rx.Component:
    return rx.el.th(
        rx.el.div(
            text,
            rx.cond(
                CustomerState.sort_column == column_key,
                rx.icon(
                    tag=rx.cond(
                        CustomerState.sort_order == "asc",
                        "chevron_up",
                        "chevron_down",
                    ),
                    size=16,
                    class_name="ml-1 text-gray-700 w-[16px]",
                ),
                rx.fragment(),
            ),
            class_name="flex items-center cursor-pointer hover:text-gray-900",
            on_click=lambda: CustomerState.sort_by_column(column_key),
        ),
        scope="col",
        class_name="px-3 py-3.5 text-left text-sm font-semibold text-gray-600",
    )


def static_table_header_cell(text: str) -> rx.Component:
    return rx.el.th(
        text,
        scope="col",
        class_name="px-3 py-3.5 text-left text-sm font-semibold text-gray-600",
    )


def customer_table_header() -> rx.Component:
    return rx.el.thead(
        rx.el.tr(
            sortable_table_header_cell("Name", "name"),
            sortable_table_header_cell("Status", "status"),
            sortable_table_header_cell("Permissions", "permissions"),
            static_table_header_cell("Email"),
            static_table_header_cell("Tags"),
            class_name="border-b border-gray-200 bg-gray-50",
        )
    )


def status_badge(status: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name=rx.match(
                status,
                (
                    "Active",
                    "h-1.5 w-1.5 rounded-full bg-blue-500",
                ),
                (
                    "Onboarding",
                    "h-1.5 w-1.5 rounded-full bg-yellow-500",
                ),
                (
                    "Pending",
                    "h-1.5 w-1.5 rounded-full bg-orange-500",
                ),
                (
                    "Suspended",
                    "h-1.5 w-1.5 rounded-full bg-red-500",
                ),
                (
                    "Inactive",
                    "h-1.5 w-1.5 rounded-full bg-gray-500",
                ),
                "h-1.5 w-1.5 rounded-full bg-gray-500",
            )
        ),
        status,
        class_name=rx.match(
            status,
            (
                "Active",
                "inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs font-medium text-blue-700 bg-blue-100 ring-1 ring-inset ring-blue-200",
            ),
            (
                "Onboarding",
                "inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs font-medium text-yellow-700 bg-yellow-100 ring-1 ring-inset ring-yellow-200",
            ),
            (
                "Pending",
                "inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs font-medium text-orange-700 bg-orange-100 ring-1 ring-inset ring-orange-200",
            ),
            (
                "Suspended",
                "inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs font-medium text-red-700 bg-red-100 ring-1 ring-inset ring-red-200",
            ),
            (
                "Inactive",
                "inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs font-medium text-gray-700 bg-gray-100 ring-1 ring-inset ring-gray-200",
            ),
            "inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs font-medium text-gray-700 bg-gray-100 ring-1 ring-inset ring-gray-200",
        ),
    )


def tag_item(tag_name: str) -> rx.Component:
    return rx.el.div(
        tag_name,
        class_name="inline-flex items-center rounded-full bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10",
    )


def customer_table_row(
    customer: CustomerData,
) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    class_name="h-6 w-6 rounded-full mr-2 sm:mr-3",
                    style={
                        "background_image": f"linear-gradient(to bottom, {customer['circle_bg_color_start']}, {customer['circle_bg_color_end']})"
                    },
                ),
                rx.el.p(
                    f"{customer['first_name']} {customer['last_name']}",
                    class_name="font-medium text-gray-900 text-sm",
                ),
                class_name="flex items-center",
            ),
            class_name="px-3 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            status_badge(customer["status"]),
            class_name="px-3 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            customer["permissions"],
            class_name="px-3 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            customer["email"],
            class_name="px-3 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.div(
                rx.cond(
                    customer["tags"].length() > 0,
                    tag_item(customer["tags"][0]),
                    rx.fragment(),
                ),
                class_name="flex items-center space-x-1 sm:space-x-2 flex-wrap gap-1",
            ),
            class_name="px-3 py-4 whitespace-nowrap text-sm",
        ),
        class_name="border-b border-gray-200 hover:bg-gray-50 cursor-pointer",
        on_click=lambda: CustomerState.select_customer_for_edit(customer),
    )


def pagination_controls() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            "Previous",
            on_click=CustomerState.prev_page,
            disabled=CustomerState.current_page <= 1,
            class_name="px-3 py-2 sm:px-4 text-xs sm:text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
        ),
        rx.el.span(
            CustomerState.current_page.to_string()
            + " / "
            + CustomerState.total_pages.to_string(),
            class_name="px-3 py-2 sm:px-4 text-xs sm:text-sm text-gray-700",
        ),
        rx.el.button(
            "Next",
            on_click=CustomerState.next_page,
            disabled=CustomerState.current_page >= CustomerState.total_pages,
            class_name="px-3 py-2 sm:px-4 text-xs sm:text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
        ),
        class_name="flex justify-center items-center mt-4 sm:mt-6 space-x-1 sm:space-x-2",
    )


def customer_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Users",
                        class_name="text-xl sm:text-2xl font-semibold text-gray-900",
                    ),
                    rx.el.span(
                        CustomerState.total_users.to_string() + " users",
                        class_name="px-2 py-0.5 sm:px-2.5 rounded-full text-xs font-medium bg-gray-100 text-gray-700",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    "See your active workplace and make changes",
                    class_name="mt-1 text-xs sm:text-sm text-gray-500",
                ),
                class_name="flex-grow",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        tag="download",
                        size=16,
                        class_name="mr-1 sm:mr-2",
                    ),
                    rx.el.span(
                        "Download CSV",
                        class_name="hidden sm:inline",
                    ),
                    rx.el.span("CSV", class_name="sm:hidden"),
                    on_click=CustomerState.download_csv,
                    class_name="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-3 py-2 sm:px-4 text-xs sm:text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 w-full sm:w-auto",
                ),
                rx.el.button(
                    rx.icon(
                        tag="plus",
                        size=16,
                        class_name="mr-1 sm:mr-2",
                    ),
                    rx.el.span(
                        "Add user",
                        class_name="hidden sm:inline",
                    ),
                    rx.el.span("Add", class_name="sm:hidden"),
                    on_click=CustomerState.prepare_add_customer,
                    class_name="inline-flex items-center justify-center rounded-md border border-transparent bg-blue-600 px-3 py-2 sm:px-4 text-xs sm:text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 w-full sm:w-auto",
                ),
                class_name="flex items-center mt-4 md:mt-0 gap-2",
            ),
            class_name="flex flex-col md:flex-row md:justify-between md:items-start mb-4 sm:mb-6 gap-4 md:gap-0",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Search by name...",
                on_change=CustomerState.set_search_query.debounce(500),
                default_value=CustomerState.search_query,
                class_name="w-full p-2 mb-4 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm",
            ),
            class_name="mb-4",
        ),
        rx.cond(
            CustomerState.loading,
            rx.el.div(
                rx.spinner(class_name="text-blue-600 h-8 w-8 sm:h-10 sm:w-10"),
                class_name="flex justify-center items-center p-6 sm:p-10 h-48 sm:h-64",
            ),
            rx.el.div(
                rx.cond(
                    CustomerState.total_db_customers == 0,
                    rx.el.p(
                        "No users found. Start by adding one!",
                        class_name="p-4 sm:p-6 text-center text-gray-600 text-sm sm:text-lg",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.table(
                                customer_table_header(),
                                rx.el.tbody(
                                    rx.foreach(
                                        CustomerState.customers,
                                        customer_table_row,
                                    ),
                                    class_name="bg-white divide-y divide-gray-200",
                                ),
                                class_name="min-w-full divide-y divide-gray-200",
                            ),
                            class_name="overflow-x-auto shadow-sm ring-1 ring-black ring-opacity-5 rounded-lg",
                        ),
                        rx.cond(
                            (CustomerState.customers.length() == 0)
                            & (CustomerState.total_db_customers > 0),
                            rx.el.p(
                                "No users to display on this page.",
                                class_name="p-4 text-center text-gray-500 mt-4 text-sm",
                            ),
                            rx.fragment(),
                        ),
                    ),
                ),
                rx.cond(
                    CustomerState.total_pages > 0,
                    pagination_controls(),
                    rx.fragment(),
                ),
            ),
        ),
        class_name="bg-white p-4 sm:p-6 shadow-lg rounded-lg",
    )
