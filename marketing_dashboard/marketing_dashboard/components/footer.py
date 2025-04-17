import reflex as rx


def footer() -> rx.Component:
    """The footer component for the dashboard."""
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "✓",
                    class_name="text-green-400 font-bold text-lg transform rotate-12",
                ),
                class_name="bg-green-900 rounded-sm p-1 mr-2 flex items-center justify-center w-6 h-6",
            ),
            rx.el.span(
                "Digital dashboard: Marketing",
                class_name="text-gray-300 font-medium",
            ),
            class_name="flex items-center text-sm max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        class_name="w-full py-4 bg-indigo-950 border-t border-gray-700 mt-8",
    )
