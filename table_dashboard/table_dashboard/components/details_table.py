import reflex as rx

from table_dashboard.states.dashboard_state import (
    DashboardState,
)


def status_badge(status: rx.Var[str]) -> rx.Component:
    """Creates a colored status badge."""
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Live",
                "px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
            ),
            (
                "Inactive",
                "px-2 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800",
            ),
            (
                "Archived",
                "px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
            ),
            "px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
        ),
    )


def table_header_cell(name: str, is_sortable: bool = True) -> rx.Component:
    """Creates a table header cell with optional sorting."""
    return rx.el.th(
        rx.el.div(
            name,
            rx.cond(
                is_sortable,
                rx.el.span(
                    rx.icon(
                        tag=rx.cond(
                            (DashboardState.sort_column == name)
                            & DashboardState.sort_ascending,
                            "arrow_upward",
                            "arrow_downward",
                        ),
                        size=14,
                        class_name=rx.cond(
                            DashboardState.sort_column == name,
                            "text-gray-800",
                            "text-gray-400 hover:text-gray-600",
                        ),
                    ),
                    class_name="ml-1 opacity-70 hover:opacity-100",
                ),
                rx.el.span(),
            ),
            class_name="flex items-center justify-between group cursor-pointer",
            on_click=rx.cond(
                is_sortable,
                DashboardState.toggle_sort(name),
                rx.noop(),
            ),
        ),
        scope="col",
        class_name="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider select-none",
    )


def details_table() -> rx.Component:
    """The main table component displaying details."""
    return rx.el.div(
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            rx.el.input(
                                type="checkbox",
                                class_name="h-4 w-4 border-gray-300 rounded text-blue-600 focus:ring-blue-500 cursor-pointer",
                                on_change=DashboardState.toggle_select_all_on_page,
                                checked=DashboardState.all_rows_on_page_selected
                                & (DashboardState.paginated_data.length() > 0),
                                disabled=DashboardState.paginated_data.length() <= 0,
                            ),
                            scope="col",
                            class_name="px-4 py-2",
                        ),
                        rx.foreach(
                            DashboardState.column_names,
                            lambda name: table_header_cell(
                                name,
                                is_sortable=name != "Edit",
                            ),
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.paginated_data,
                        lambda row: rx.el.tr(
                            rx.el.td(
                                rx.el.input(
                                    type="checkbox",
                                    class_name="h-4 w-4 border-gray-300 rounded text-blue-600 focus:ring-blue-500 cursor-pointer",
                                    on_change=lambda: DashboardState.toggle_row_selection(
                                        row["id"]
                                    ),
                                    checked=DashboardState.selected_rows.contains(
                                        row["id"]
                                    ),
                                ),
                                class_name="px-4 py-2 whitespace-nowrap",
                            ),
                            rx.el.td(
                                row["owner"],
                                class_name="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900",
                            ),
                            rx.el.td(
                                status_badge(row["status"]),
                                class_name="px-4 py-2 whitespace-nowrap text-sm",
                            ),
                            rx.el.td(
                                row["region"],
                                class_name="px-4 py-2 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                row["stability"].to_string(),
                                class_name="px-4 py-2 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                "$" + row["costs"].to_string(),
                                class_name="px-4 py-2 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                row["last_edited"],
                                class_name="px-4 py-2 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                rx.el.button(
                                    rx.icon(
                                        tag="send_horizontal",
                                        size=16,
                                    ),
                                    variant="ghost",
                                    class_name="text-gray-400 hover:text-gray-600",
                                ),
                                class_name="px-4 py-2 whitespace-nowrap text-right text-sm font-medium",
                            ),
                            class_name="hover:bg-gray-50",
                        ),
                    )
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="overflow-x-auto",
        ),
        rx.el.div(
            rx.el.p(
                DashboardState.selected_rows.length().to_string()
                + " of "
                + DashboardState.total_rows.to_string()
                + " row(s) selected.",
                class_name="text-sm text-gray-500",
            ),
            rx.el.div(
                rx.el.span(
                    "Showing "
                    + DashboardState.current_rows_display
                    + " of "
                    + DashboardState.total_rows.to_string(),
                    class_name="text-sm text-gray-500 mr-4",
                ),
                rx.el.button(
                    rx.icon(tag="chevron_left", size=18),
                    on_click=DashboardState.previous_page,
                    disabled=DashboardState.current_page <= 1,
                    class_name="p-1 border border-gray-300 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50",
                ),
                rx.el.button(
                    rx.icon(tag="chevron_right", size=18),
                    on_click=DashboardState.next_page,
                    disabled=DashboardState.current_page >= DashboardState.total_pages,
                    class_name="p-1 border border-gray-300 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 ml-2",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between mt-4 px-4 py-2 border-t border-gray-200",
        ),
        class_name="border border-gray-200 rounded",
    )
