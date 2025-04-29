import reflex as rx


def sidebar_item(
    text: str,
    icon: str,
    href: str = "#",
    is_active: bool = False,
) -> rx.Component:
    """A reusable sidebar item component."""
    return rx.el.a(
        rx.icon(tag=icon, class_name="mr-3 size-4"),
        rx.el.label(text, class_name="text-sm"),
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center px-4 py-2 text-sm font-medium text-gray-900 bg-gray-100 rounded-lg",
            "flex items-center px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900 rounded-lg",
        ),
    )


def sidebar() -> rx.Component:
    """The sidebar component for the dashboard."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Reflex Build",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.label(
                    "v.0.0.1",
                    class_name="text-sm font-regular text-gray-500",
                ),
                class_name="flex items-center px-2 h-12 justify-between",
            ),
            rx.el.label(
                "Projects",
                class_name="px-4 mb-2 text-sm font-semibold tracking-wider text-gray-500 uppercase",
            ),
            rx.el.nav(
                sidebar_item(
                    "Dashboard",
                    "layout-dashboard",
                    is_active=True,
                ),
                sidebar_item("Lifecycle", "recycle"),
                sidebar_item("Analytics", "bar-chart-3"),
                sidebar_item("Projects", "folder"),
                sidebar_item("Team", "users"),
                class_name="space-y-1 mb-6 pt-2",
            ),
            rx.el.label(
                "Documents",
                class_name="px-4 mb-2 text-sm font-semibold tracking-wider text-gray-500 uppercase",
            ),
            rx.el.nav(
                sidebar_item("Data Library", "database"),
                sidebar_item("Reports", "file-text"),
                sidebar_item("Word Assistant", "file-input"),
                sidebar_item("More", "send_horizontal"),
                class_name="space-y-1",
            ),
        ),
        class_name="max-md:hidden flex flex-col justify-between w-[280px] h-screen px-2 bg-white border-r border-gray-200 sticky",
    )
