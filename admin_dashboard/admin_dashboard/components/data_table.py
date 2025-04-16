import reflex as rx

from admin_dashboard.states.dashboard_state import (
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
    """Displays sort direction icon if the column is being sorted."""
    return rx.cond(
        DashboardState.sort_column == column_key,
        rx.match(
            DashboardState.sort_order,
            (
                "asc",
                rx.icon(
                    "arrow-up",
                    size=12,
                    class_name="ml-1 inline",
                ),
            ),
            (
                "desc",
                rx.icon(
                    "arrow-down",
                    size=12,
                    class_name="ml-1 inline",
                ),
            ),
            rx.el.span(),
        ),
        rx.el.span(),
    )


def table_header(col: str) -> rx.Component:
    """Renders a table header cell, making it clickable for sorting if applicable."""
    base_class = "px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider"
    sortable_columns: dict[str, SortColumn] = {
        "Next renewal": "next_renewal",
        "Revenue": "revenue",
        "Licenses": "licenses",
        "Active licenses": "active_licenses",
    }
    is_sortable = col in sortable_columns
    column_key = sortable_columns.get(col)
    text_align_class = rx.match(
        col,
        ("Revenue", "text-right"),
        (
            (
                "Licenses",
                "Active licenses",
                "Active license growth",
            ),
            "text-center",
        ),
        "text-left",
    )
    justify_content_val = rx.match(
        col,
        ("Revenue", "flex-end"),
        (
            (
                "Licenses",
                "Active licenses",
                "Active license growth",
            ),
            "center",
        ),
        "flex-start",
    )
    combined_class = f"{base_class} {text_align_class}"
    return rx.cond(
        is_sortable & (column_key is not None),
        rx.el.th(
            rx.el.div(
                col,
                sort_icon(column_key),
                class_name="flex items-center cursor-pointer hover:text-gray-700 transition-colors duration-150 ease-in-out",
                style={"justify_content": justify_content_val},
            ),
            scope="col",
            class_name=combined_class,
            on_click=lambda: DashboardState.sort_by(column_key),
        ),
        rx.el.th(col, scope="col", class_name=combined_class),
    )


def data_table() -> rx.Component:
    """The main data table component."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Search by customer name",
                    on_change=DashboardState.set_search_term.debounce(300),
                    default_value=DashboardState.search_term,
                    key=f"search-input-{DashboardState.search_term}",
                    class_name="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-sm text-gray-800",
                ),
                class_name="relative mb-4",
            )
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.foreach(
                            DashboardState.table_columns,
                            table_header,
                        ),
                        class_name="bg-gray-50",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.filtered_customers,
                        lambda customer: rx.el.tr(
                            rx.el.td(
                                customer["id"],
                                class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-700 text-left",
                            ),
                            rx.el.td(
                                customer["customer_name"],
                                class_name="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900 text-left",
                            ),
                            rx.el.td(
                                customer["next_renewal"],
                                class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-700 text-left",
                            ),
                            rx.el.td(
                                rx.el.span(
                                    "$",
                                    customer["revenue"].to_string(),
                                ),
                                class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-700 text-right",
                            ),
                            rx.el.td(
                                customer["licenses"],
                                class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-700 text-center",
                            ),
                            rx.el.td(
                                customer["active_licenses"],
                                class_name="px-4 py-3 whitespace-nowrap text-sm text-gray-700 text-center",
                            ),
                            rx.el.td(
                                rx.el.span(
                                    rx.cond(
                                        customer["active_license_growth"] > 0,
                                        "+",
                                        "",
                                    ),
                                    customer["active_license_growth"],
                                    "%",
                                ),
                                class_name=rx.cond(
                                    customer["active_license_growth"] > 0,
                                    "px-4 py-3 whitespace-nowrap text-sm text-green-600 text-center",
                                    "px-4 py-3 whitespace-nowrap text-sm text-red-600 text-center",
                                ),
                            ),
                            rx.el.td(
                                industry_tag(customer["industry"]),
                                class_name="px-4 py-3 whitespace-nowrap text-sm text-left",
                            ),
                            rx.el.td(
                                platform_tag(customer["platform"]),
                                class_name="px-4 py-3 whitespace-nowrap text-sm text-left",
                            ),
                            on_click=lambda: DashboardState.select_customer(
                                customer["id"]
                            ),
                            class_name=rx.cond(
                                DashboardState.selected_customer_id == customer["id"],
                                "bg-emerald-50 border-l-4 border-emerald-500 cursor-pointer hover:bg-emerald-100 transition-colors duration-150 ease-in-out",
                                "border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors duration-150 ease-in-out",
                            ),
                        ),
                    )
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg overflow-x-auto",
        ),
        rx.el.div(
            rx.el.p(
                DashboardState.result_count.to_string() + " results",
                class_name="text-sm text-gray-500 mt-4",
            ),
            class_name="flex justify-end",
        ),
        class_name="bg-white p-6 rounded-lg shadow-md",
    )
