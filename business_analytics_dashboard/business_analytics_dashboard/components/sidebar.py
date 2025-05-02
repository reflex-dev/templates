import reflex as rx


def sidebar_link(text: str, url: str, is_active: bool) -> rx.Component:
    """Creates a sidebar link component."""
    return rx.el.a(
        rx.el.div(
            text,
            class_name=rx.cond(
                is_active,
                "bg-gray-200 px-4 py-2 rounded-md cursor-pointer",
                "hover:bg-gray-50 px-4 py-2 rounded-md cursor-pointer transition-colors",
            ),
        ),
        href=url,
        class_name="w-full",
    )


def sidebar() -> rx.Component:
    """The sidebar component for the dashboard."""
    return rx.el.div(
        rx.el.div(
            rx.el.label("Analytics", class_name="text-lg font-bold"),
            class_name="px-6 py-2 mb-4 flex justify-start",
        ),
        rx.el.nav(
            sidebar_link("Sales Performance", "#", False),
            sidebar_link("Business Analytics", "#", True),
            sidebar_link("Financial Reporting", "#", False),
            sidebar_link("Marketing Analytics", "#", False),
            class_name="flex flex-col space-y-2 p-2",
        ),
        class_name="w-full max-w-[250px] border-r-1 border-gray-200 h-screen sticky top-0 left-0 max-lg:hidden",
    )
