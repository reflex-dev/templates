import reflex as rx

from retail_dashboard.states.dashboard_state import DashboardState


def nav_link(
    text: str,
    icon_name: str,
    href: str | None = None,
    on_click: rx.event.EventHandler | None = None,
) -> rx.Component:
    """A reusable navigation link component."""
    current_path_check = rx.cond(href, DashboardState.router.page.path == href, False)
    base_class = "flex items-center px-3.5 py-2.5 text-sm rounded-lg"
    active_class = f"{base_class} font-medium text-neutral-700 bg-neutral-100"
    inactive_class = f"{base_class} text-gray-600 hover:bg-gray-100 hover:text-gray-800"
    icon_active_class = "text-neutral-700"
    icon_inactive_class = "text-gray-400 group-hover:text-gray-500"
    link_content = rx.el.span(
        rx.icon(
            tag=icon_name,
            size=18,
            class_name=rx.cond(
                current_path_check,
                icon_active_class,
                icon_inactive_class,
            )
            + " mr-3.5",
        ),
        text,
        class_name=rx.cond(current_path_check, active_class, inactive_class)
        + " group w-full",
        on_click=rx.cond(on_click, on_click, rx.noop()),
    )
    if href:
        return rx.el.a(
            link_content,
            href=href,
            class_name="cursor-pointer",
        )
    else:
        return rx.el.button(
            link_content,
            class_name="w-full text-left cursor-pointer",
        )


def sidebar() -> rx.Component:
    """A simple static sidebar component."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon(tag="store", size=20),
                class_name="text-white font-bold text-lg mr-3 p-2.5 bg-neutral-600 rounded-lg",
            ),
            rx.el.div(
                rx.el.p(
                    "Retail Shop",
                    class_name="font-semibold text-gray-800 text-sm",
                ),
                rx.el.p(
                    "Admin",
                    class_name="text-xs text-gray-500 mt-0.5",
                ),
                class_name="flex-grow",
            ),
            class_name="flex items-center py-6 px-4 border-b border-gray-200",
        ),
        rx.el.nav(
            nav_link("Dashboard", "layout_dashboard", href="/"),
            class_name="flex-grow p-3.5 space-y-2",
        ),
        class_name="w-full max-w-[260px] border-r border-gray-200 bg-white flex flex-col h-screen sticky top-0 left-0 max-lg:hidden",
    )
