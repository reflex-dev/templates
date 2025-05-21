import reflex as rx

from retail_dashboard.components.filter_dropdown import (
    costs_filter_dropdown,
    country_filter_dropdown,
    filter_button,
    status_filter_dropdown,
)
from retail_dashboard.states.dashboard_state import DashboardState


def header() -> rx.Component:
    """The header component with title, filters, and actions."""
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Dashboard",
                class_name="text-2xl font-semibold text-gray-800",
            ),
            rx.el.p(
                "Manage and analyze your retail data entries.",
                class_name="text-sm text-gray-500 mt-1.5",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    filter_button(
                        "Status",
                        on_click=DashboardState.toggle_status_filter,
                        is_active=DashboardState.show_status_filter,
                        has_filter=DashboardState.selected_statuses.length() > 0,
                    ),
                    status_filter_dropdown(),
                    class_name="relative",
                ),
                rx.el.div(
                    filter_button(
                        "Country",
                        on_click=DashboardState.toggle_country_filter,
                        is_active=DashboardState.show_country_filter,
                        has_filter=DashboardState.selected_countries.length() > 0,
                    ),
                    country_filter_dropdown(),
                    class_name="relative",
                ),
                rx.el.div(
                    filter_button(
                        "Costs",
                        on_click=DashboardState.toggle_costs_filter,
                        is_active=DashboardState.show_costs_filter,
                        has_filter=DashboardState.min_cost | DashboardState.max_cost,
                    ),
                    costs_filter_dropdown(),
                    class_name="relative",
                ),
                rx.el.button(
                    "Reset Filters",
                    on_click=DashboardState.reset_all_filters,
                    class_name="px-4 py-2.5 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-1 focus:ring-gray-400",
                    disabled=(DashboardState.search_owner == "")
                    & (DashboardState.selected_statuses.length() == 0)
                    & (DashboardState.selected_countries.length() == 0)
                    & (DashboardState.min_cost.is_none())
                    & (DashboardState.max_cost.is_none()),
                ),
                class_name="flex items-center space-x-2.5 flex-wrap gap-y-2.5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        tag="search",
                        size=18,
                        class_name="absolute left-3.5 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none",
                    ),
                    rx.el.input(
                        placeholder="Search by owner...",
                        on_change=DashboardState.set_search_owner.debounce(300),
                        class_name="pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-neutral-500 focus:border-neutral-500 w-full sm:w-80",
                        default_value=DashboardState.search_owner,
                    ),
                    class_name="relative flex items-center",
                ),
                rx.el.button(
                    rx.icon(
                        tag="cloud_download",
                        size=16,
                        class_name="mr-2",
                    ),
                    "Export CSV",
                    on_click=DashboardState.download_csv,
                    disabled=DashboardState.filtered_and_sorted_data.length() <= 0,
                    class_name="flex items-center px-4 py-2.5 rounded-lg text-sm font-medium text-white bg-neutral-600 hover:bg-neutral-700 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-neutral-500",
                ),
                class_name="flex items-center space-x-2.5",
            ),
            class_name="flex items-center justify-between flex-wrap gap-y-3.5 mt-5",
        ),
        class_name="pb-3 md:pb-6 border-b border-gray-200",
    )
