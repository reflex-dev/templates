from admin_dashboard.states.dashboard_state import DashboardState, SortColumn

import reflex as rx

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