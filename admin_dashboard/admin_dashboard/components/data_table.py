from typing import Optional, Tuple

import reflex as rx

from admin_dashboard.states.dashboard_state import (
    CustomerData,
    DashboardState,
    SortColumn,
)


def platform_tag(platform: rx.Var[str]) -> rx.Component:
    """Renders a colored tag based on the platform."""
    return rx.el.span(
        platform,
        class_name=rx.match(
            platform,
            (
                "Windows",
                "px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800",
            ),
            (
                "macOS",
                "px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800",
            ),
            (
                "iOS",
                "px-2 py-1 text-xs font-medium rounded-full bg-yellow-100 text-yellow-800",
            ),
            "px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800",
        ),
    )


def industry_tag(industry: rx.Var[str]) -> rx.Component:
    """Renders a colored tag based on the industry."""
    return rx.el.span(
        industry,
        class_name=rx.match(
            industry,
            (
                "Finance",
                "px-2 py-1 text-xs font-medium rounded-full bg-pink-100 text-pink-800",
            ),
            (
                "Healthcare",
                "px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-800",
            ),
            (
                "Education",
                "px-2 py-1 text-xs font-medium rounded-full bg-orange-100 text-orange-800",
            ),
            "px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800",
        ),
    )


def sort_icon(column_key: SortColumn) -> rx.Component:
    """Displays sort direction icon or a neutral sortable indicator."""
    icon_base_class = (
        "ml-1 inline-block w-3 h-3 transition-colors duration-150 ease-in-out"
    )
    active_icon_class = f"{icon_base_class} text-gray-700"
    inactive_icon_class = f"{icon_base_class} text-gray-400 group-hover:text-gray-600"
    is_active_column = DashboardState.sort_column == column_key
    return rx.cond(
        is_active_column,
        rx.cond(
            DashboardState.sort_order == "asc",
            rx.icon(
                "arrow-up",
                size=12,
                class_name=active_icon_class,
            ),
            rx.icon(
                "arrow-down",
                size=12,
                class_name=active_icon_class,
            ),
        ),
        rx.icon(
            "chevrons-up-down",
            size=12,
            class_name=inactive_icon_class,
        ),
    )


def sortable_table_header(col_name: str, column_key: SortColumn) -> rx.Component:
    """Renders a sortable table header cell."""
    base_class = "px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider group"
    sortable_class = f"{base_class} cursor-pointer"
    text_align_class = rx.match(
        col_name,
        ("Revenue", "text-right"),
        ("Licenses", "text-center"),
        ("Active licenses", "text-center"),
        "text-left",
    )
    justify_content_val = rx.match(
        col_name,
        ("Revenue", "flex-end"),
        ("Licenses", "center"),
        ("Active licenses", "center"),
        "flex-start",
    )
    combined_class = f"{sortable_class} {text_align_class}"
    header_content_inner = rx.el.div(
        col_name,
        sort_icon(column_key),
        class_name="flex items-center group-hover:text-gray-700 transition-colors duration-150 ease-in-out",
        style={"justify_content": justify_content_val},
    )
    return rx.el.th(
        header_content_inner,
        scope="col",
        class_name=combined_class,
        on_click=lambda: DashboardState.sort_by(column_key),
    )


def non_sortable_table_header(
    col_name: str,
) -> rx.Component:
    """Renders a non-sortable table header cell."""
    base_class = (
        "px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
    )
    text_align_class = rx.match(
        col_name,
        ("Revenue", "text-right"),
        ("Licenses", "text-center"),
        ("Active licenses", "text-center"),
        "text-left",
    )
    justify_content_val = rx.match(
        col_name,
        ("Revenue", "flex-end"),
        ("Licenses", "center"),
        ("Active licenses", "center"),
        "flex-start",
    )
    combined_class = f"{base_class} {text_align_class}"
    header_content_inner = rx.el.div(
        col_name,
        class_name="flex items-center",
        style={"justify_content": justify_content_val},
    )
    return rx.el.th(
        header_content_inner,
        scope="col",
        class_name=combined_class,
    )


def table_header(
    col_data: rx.Var[Tuple[str, Optional[SortColumn]]],
) -> rx.Component:
    """Renders a table header cell, deciding if it's sortable or not."""
    col_name = col_data[0]
    column_key = col_data[1]
    return rx.cond(
        column_key,
        sortable_table_header(col_name, column_key.to(SortColumn)),
        non_sortable_table_header(col_name),
    )


def get_cell_content(col_name: rx.Var[str], customer: CustomerData) -> rx.Component:
    """Gets the appropriate component for a specific cell based on column name."""
    base_class = "px-4 py-3 whitespace-nowrap text-sm"
    return rx.match(
        col_name,
        (
            "ID",
            rx.el.td(
                customer["id"],
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Customer name",
            rx.el.td(
                customer["customer_name"],
                class_name=f"{base_class} font-medium text-gray-900 text-left",
            ),
        ),
        (
            "Next renewal",
            rx.el.td(
                customer["next_renewal"],
                class_name=f"{base_class} text-gray-700 text-left",
            ),
        ),
        (
            "Revenue",
            rx.el.td(
                "$" + customer["revenue"].to_string(),
                class_name=f"{base_class} text-gray-700 text-right",
            ),
        ),
        (
            "Licenses",
            rx.el.td(
                customer["licenses"],
                class_name=f"{base_class} text-gray-700 text-center",
            ),
        ),
        (
            "Active licenses",
            rx.el.td(
                customer["active_licenses"],
                class_name=f"{base_class} text-gray-700 text-center",
            ),
        ),
        (
            "Active license growth",
            rx.el.td(
                rx.cond(
                    customer["active_license_growth"] > 0,
                    "+",
                    "",
                )
                + customer["active_license_growth"].to_string()
                + "%",
                class_name=rx.cond(
                    customer["active_license_growth"] > 0,
                    f"{base_class} text-green-600 text-center",
                    f"{base_class} text-red-600 text-center",
                ),
            ),
        ),
        (
            "Industry",
            rx.el.td(
                industry_tag(customer["industry"]),
                class_name=f"{base_class} text-left",
            ),
        ),
        (
            "Platform",
            rx.el.td(
                platform_tag(customer["platform"]),
                class_name=f"{base_class} text-left",
            ),
        ),
        rx.el.td(
            "-",
            class_name=f"{base_class} text-gray-500 text-left",
        ),
    )


def table_row(customer: CustomerData) -> rx.Component:
    """Renders a single row in the data table."""
    return rx.el.tr(
        rx.foreach(
            DashboardState.column_data,
            lambda col_data: get_cell_content(col_data[0], customer),
        ),
        on_click=lambda: DashboardState.select_customer(customer["id"]),
        class_name=rx.cond(
            DashboardState.selected_customer_id == customer["id"],
            "w-full bg-emerald-50 border-l-4 border-emerald-500 cursor-pointer hover:bg-emerald-100 transition-colors duration-150 ease-in-out",
            "w-full border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors duration-150 ease-in-out",
        ),
    )


def data_table() -> rx.Component:
    """The main data table component including search and results count."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    size=20,
                    class_name="text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2 pointer-events-none",
                ),
                rx.el.input(
                    placeholder="Search by customer name...",
                    default_value=DashboardState.search_term,
                    on_change=DashboardState.set_search_term.debounce(300),
                    class_name="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-sm text-gray-800 placeholder-gray-500",
                ),
                class_name="relative flex-grow",
            ),
            class_name="flex items-center gap-4 mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.foreach(
                            DashboardState.column_data,
                            table_header,
                        ),
                        class_name="bg-gray-50 border-b border-gray-200 whitespace-nowrap",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.filtered_customers,
                        table_row,
                    ),
                    rx.cond(
                        DashboardState.result_count == 0,
                        rx.el.tr(
                            rx.el.td(
                                "No customers found matching your criteria.",
                                col_span=DashboardState.column_data.length(),
                                class_name="px-4 py-3 text-center text-gray-500 italic",
                            )
                        ),
                        rx.fragment(),
                    ),
                    class_name="divide-y divide-gray-200",
                ),
                class_name="min-w-full",
            ),
            class_name="shadow overflow-hidden border border-gray-200 sm:rounded-lg overflow-x-auto",
        ),
        rx.el.div(
            rx.el.p(
                DashboardState.result_count.to_string() + " results",
                class_name="text-sm text-gray-500 mt-4",
            ),
            class_name="flex justify-end",
        ),
        class_name="bg-white p-6 rounded-lg shadow-md col-span-1 md:col-span-2",
    )
