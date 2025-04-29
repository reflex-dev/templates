import reflex as rx

from company_dashboard.states.dashboard_state import (
    DashboardState,
)


def document_tab_button(text: str, count: int = 0) -> rx.Component:
    """Button for selecting document table tabs."""
    return rx.el.button(
        text,
        rx.cond(
            count > 0,
            rx.el.span(
                count,
                class_name="ml-1.5 px-1.5 py-0.5 text-xs font-medium rounded-full bg-gray-200 text-gray-600",
            ),
            rx.fragment(),
        ),
        on_click=lambda: DashboardState.set_document_tab(text),
        class_name=rx.cond(
            DashboardState.selected_document_tab == text,
            "px-3 py-1.5 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md shadow-sm",
            "px-3 py-1.5 text-sm font-medium text-gray-500 bg-white border border-transparent rounded-md hover:bg-gray-50 hover:text-gray-700",
        ),
    )


def status_badge(status: rx.Var[str]) -> rx.Component:
    """Displays a status badge based on the status string."""
    return rx.el.span(
        rx.icon(
            tag=rx.match(
                status,
                ("Done", "check-circle"),
                ("In Process", "loader"),
                ("Pending", "alert-circle"),
                "help-circle",
            ),
            class_name="mr-1.5 size-4",
        ),
        status,
        class_name=rx.match(
            status,
            (
                "Done",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
            ),
            (
                "In Process",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800",
            ),
            (
                "Pending",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800",
            ),
            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
        ),
    )


def documents_table_section() -> rx.Component:
    """The section displaying the documents table."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                document_tab_button("Outline"),
                document_tab_button("Past Performance", 3),
                document_tab_button("Key Personnel", 2),
                document_tab_button("Focus Documents"),
                class_name="flex flex-row flex-wrap items-center gap-2 justify-start pb-2",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        tag="list-filter",
                        class_name="w-4 h-4 mr-2",
                    ),
                    "Customize Columns",
                    rx.icon(
                        tag="chevron-down",
                        class_name="w-4 h-4 ml-1",
                    ),
                    class_name="flex items-center px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50",
                ),
                rx.el.button(
                    rx.icon(
                        tag="plus",
                        class_name="w-4 h-4 mr-2",
                    ),
                    "Add Section",
                    class_name="flex items-center px-3 py-1.5 text-sm font-medium text-white bg-gray-800 border border-transparent rounded-md shadow-sm hover:bg-gray-700",
                ),
                class_name="flex items-center space-x-3",
            ),
            class_name="flex flex-wrap items-center justify-between mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.foreach(
                            DashboardState.document_columns,
                            lambda col_name: rx.el.th(
                                col_name,
                                scope="col",
                                class_name="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                        )
                    ),
                    class_name="bg-gray-50",
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.document_data,
                        lambda row: rx.el.tr(
                            rx.el.td(
                                rx.el.div(
                                    rx.icon(
                                        tag="grip-vertical",
                                        class_name="w-4 h-4 text-gray-400 mr-3 cursor-grab",
                                    ),
                                    rx.el.input(
                                        type="checkbox",
                                        class_name="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500",
                                    ),
                                    class_name="flex items-center",
                                ),
                                class_name="px-4 py-3 whitespace-nowrap",
                            ),
                            rx.el.td(
                                row["header"],
                                class_name="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900",
                            ),
                            rx.el.td(
                                row["section_type"],
                                class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                status_badge(row["status"]),
                                class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                row["target"],
                                class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                row["limit"],
                                class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                row["reviewer"],
                                class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-500",
                            ),
                        ),
                    ),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="overflow-x-auto border border-gray-200 rounded-lg shadow-sm",
        ),
        class_name="p-5 bg-white border border-gray-200 rounded-lg shadow-sm mt-5",
    )
