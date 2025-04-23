import reflex as rx


def header_bar() -> rx.Component:
    """The header bar component."""
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "reflex > build > ",
                class_name="text-sm font-semibold text-gray-500",
            ),
            rx.el.label(
                "dashboard",
                class_name="text-sm font-semibold text-gray-900",
            ),
        ),
        rx.el.div(),
        class_name="flex items-center justify-between h-12 px-6 bg-white border-b border-gray-200",
    )
