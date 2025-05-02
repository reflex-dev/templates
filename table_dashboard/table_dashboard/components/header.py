import reflex as rx

from table_dashboard.components.filter_dropdown import (
    costs_filter_dropdown,
    filter_button,
    region_filter_dropdown,
    status_filter_dropdown,
)
from table_dashboard.states.dashboard_state import DashboardState


def header() -> rx.Component:
    """The header component with title, filters, and actions."""
    return rx.el.div(
        rx.el.h1(
            "Details",
            class_name="text-2xl font-semibold text-gray-900 mb-4",
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
                        "Region",
                        on_click=DashboardState.toggle_region_filter,
                        is_active=DashboardState.show_region_filter,
                        has_filter=DashboardState.selected_regions.length() > 0,
                    ),
                    region_filter_dropdown(),
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
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            tag="search",
                            size=18,
                            class_name="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Search by owner...",
                            on_change=DashboardState.set_search_owner.debounce(300),
                            class_name="pl-10 pr-4 py-1.5 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500",
                            default_value=DashboardState.search_owner,
                        ),
                        class_name="relative flex items-center -ml-2 sm:ml-0",
                    ),
                    rx.el.button(
                        "Reset All",
                        on_click=DashboardState.reset_all_filters,
                        class_name="px-3 py-1.5 border border-gray-300 rounded text-sm text-gray-700 hover:bg-gray-50",
                        disabled=(DashboardState.search_owner == "")
                        & (DashboardState.selected_statuses.length() == 0)
                        & (DashboardState.selected_regions.length() == 0)
                        & (DashboardState.min_cost is None)
                        & (DashboardState.max_cost is None),
                    ),
                    class_name="flex flex-row items-center justify-start gap-x-2",
                ),
                class_name="flex items-center space-x-2 flex-wrap gap-y-2",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        tag="upload",
                        size=16,
                        class_name="mr-1.5",
                    ),
                    "Export",
                    on_click=DashboardState.download_csv,
                    disabled=DashboardState.filtered_and_sorted_data.length() <= 0,
                    class_name="flex items-center px-3 py-1.5 border border-gray-300 rounded text-sm text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
                ),
                rx.el.button(
                    rx.icon(
                        tag="eye",
                        size=16,
                        class_name="mr-1.5",
                    ),
                    "View",
                    class_name="flex items-center px-3 py-1.5 border border-gray-300 rounded text-sm text-gray-700 hover:bg-gray-50",
                ),
                class_name="flex items-center space-x-2",
            ),
            class_name="flex items-center justify-between flex-wrap gap-y-3",
        ),
    )
