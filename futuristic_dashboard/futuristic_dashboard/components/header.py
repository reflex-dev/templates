import reflex as rx

from futuristic_dashboard.states.dashboard_state import DashboardState


def dashboard_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon(tag="menu", class_name="size-6"),
                on_click=DashboardState.toggle_mobile_sidebar,
                class_name="p-2 text-gray-400 hover:text-gray-200 md:hidden mr-4",
            ),
            rx.el.div(
                rx.icon(
                    tag="search",
                    class_name="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 pointer-events-none",
                ),
                rx.el.input(
                    placeholder="Search systems...",
                    class_name="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 placeholder-gray-500",
                ),
                class_name="relative flex-grow max-w-xs hidden sm:block",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon(
                    tag="bell",
                    class_name="text-gray-400 hover:text-gray-200",
                ),
                class_name="p-2 rounded-full hover:bg-gray-800",
            ),
            rx.el.button(
                rx.icon(
                    tag="moon",
                    class_name="text-gray-400 hover:text-gray-200",
                ),
                class_name="p-2 rounded-full hover:bg-gray-800",
            ),
            rx.el.div(
                class_name="w-8 h-8 rounded-full bg-cyan-500 ml-3 hidden sm:block"
            ),
            class_name="flex items-center space-x-1 sm:space-x-3",
        ),
        class_name="sticky top-0 z-30 flex items-center justify-between p-4 border-b border-gray-700/50 bg-gray-950/80 backdrop-blur-md",
    )
