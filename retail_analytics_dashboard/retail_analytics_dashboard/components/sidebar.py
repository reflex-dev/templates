import reflex as rx

from retail_analytics_dashboard.states.dashboard_state import DashboardState


def sidebar_nav_item(item: rx.Var[dict]) -> rx.Component:
    """Renders a single navigation item in the sidebar."""
    return rx.el.a(
        rx.icon(tag=item["icon"], class_name="w-5 h-5 mr-3"),
        item["name"],
        href="#",
        on_click=lambda: DashboardState.set_active_nav(item["name"]),
        class_name=rx.cond(
            item["active"],
            "flex items-center px-4 py-2 text-sm font-medium text-indigo-700 bg-indigo-100 rounded-md transition-colors duration-150",
            "flex items-center px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-md transition-colors duration-150",
        ),
    )


def sidebar_shortcut_item(
    item: rx.Var[dict],
) -> rx.Component:
    """Renders a single shortcut item in the sidebar."""
    return rx.el.a(
        rx.icon(
            tag=item["icon"],
            class_name="w-5 h-5 mr-3 text-gray-400",
        ),
        item["name"],
        href="#",
        class_name="flex items-center px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-md transition-colors duration-150",
    )


def sidebar() -> rx.Component:
    """The sidebar component for the dashboard."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        "RA",
                        class_name="w-10 h-10 bg-indigo-600 text-white flex items-center justify-center rounded-md text-sm font-semibold",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Retail analytics",
                            class_name="text-sm font-semibold text-gray-800",
                        ),
                        rx.el.p(
                            "Member",
                            class_name="text-xs text-gray-500",
                        ),
                        class_name="ml-3",
                    ),
                    rx.el.button(
                        rx.icon(
                            tag="chevrons-up-down",
                            class_name="w-4 h-4",
                        ),
                        class_name="ml-auto text-gray-400 hover:text-gray-600 focus:outline-none",
                    ),
                    class_name="flex items-center p-4 border-b border-gray-200",
                )
            ),
            rx.el.nav(
                rx.foreach(
                    DashboardState.nav_items,
                    sidebar_nav_item,
                ),
                class_name="px-4 py-4 space-y-1",
            ),
            rx.el.div(
                rx.el.h3(
                    "Shortcuts",
                    class_name="px-4 pt-4 pb-2 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                ),
                rx.el.div(
                    rx.foreach(
                        DashboardState.shortcuts,
                        sidebar_shortcut_item,
                    ),
                    class_name="px-4 space-y-1",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        "ES",
                        class_name="w-8 h-8 bg-gray-200 text-gray-600 flex items-center justify-center rounded-full text-xs font-semibold",
                    ),
                    rx.el.p(
                        "Emma Stone",
                        class_name="ml-3 text-sm font-medium text-gray-800",
                    ),
                    rx.el.button(
                        rx.icon(
                            tag="send_horizontal",
                            class_name="w-4 h-4",
                        ),
                        class_name="ml-auto text-gray-400 hover:text-gray-600 focus:outline-none",
                    ),
                    class_name="flex items-center p-4",
                ),
                class_name="mt-auto border-t border-gray-200",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="hidden lg:flex w-64 border-r border-gray-200 flex-shrink-0 sticky top-0 h-screen overflow-y-auto",
    )
