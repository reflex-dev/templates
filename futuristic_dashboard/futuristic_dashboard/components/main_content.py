import reflex as rx

from futuristic_dashboard.components.charts import (
    performance_line_chart,
    stat_card_chart,
)
from futuristic_dashboard.states.dashboard_state import (
    DashboardState,
    StatCardData,
)


def stat_card(card_data: StatCardData) -> rx.Component:
    color = card_data["color"]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    card_data["title"],
                    class_name="text-sm font-medium text-gray-400",
                ),
                rx.el.p(
                    card_data["value"],
                    class_name="text-2xl font-bold text-gray-100 mt-1",
                ),
                rx.el.p(
                    card_data["sub_detail"],
                    class_name="text-xs text-gray-500 mt-1",
                ),
            ),
            rx.el.div(
                rx.icon(
                    tag=card_data["icon"],
                    class_name="size-6",
                ),
                class_name=f"p-3 rounded-lg bg-gradient-to-br from-{color}-500 to-{color}-600 text-white shadow-lg",
            ),
            class_name="flex justify-between items-start mb-3",
        ),
        stat_card_chart(card_data["chart_data"], card_data["color"]),
        class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm hover:bg-gray-800/70 transition-colors duration-200",
    )


def performance_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                "Performance",
                on_click=lambda: DashboardState.set_active_performance_tab(
                    "Performance"
                ),
                class_name=rx.cond(
                    DashboardState.active_performance_tab == "Performance",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-white bg-cyan-600 rounded-md focus:outline-none",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-gray-400 hover:text-gray-200 hover:bg-gray-700 rounded-md focus:outline-none transition-colors duration-150",
                ),
            ),
            rx.el.button(
                "Processes",
                on_click=lambda: DashboardState.set_active_performance_tab("Processes"),
                class_name=rx.cond(
                    DashboardState.active_performance_tab == "Processes",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-white bg-cyan-600 rounded-md focus:outline-none",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-gray-400 hover:text-gray-200 hover:bg-gray-700 rounded-md focus:outline-none transition-colors duration-150",
                ),
            ),
            rx.el.button(
                "Storage",
                on_click=lambda: DashboardState.set_active_performance_tab("Storage"),
                class_name=rx.cond(
                    DashboardState.active_performance_tab == "Storage",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-white bg-cyan-600 rounded-md focus:outline-none",
                    "px-3 py-2 text-xs sm:px-4 sm:py-2 sm:text-sm font-medium text-gray-400 hover:text-gray-200 hover:bg-gray-700 rounded-md focus:outline-none transition-colors duration-150",
                ),
            ),
            class_name="flex space-x-1 border-b border-gray-700/50 mb-4 pb-2 overflow-x-auto",
        ),
        rx.el.div(
            rx.cond(
                DashboardState.active_performance_tab == "Performance",
                rx.el.div(
                    performance_line_chart(DashboardState.performance_chart_data),
                    rx.el.div(
                        rx.el.p(
                            "System Load",
                            class_name="text-xs text-gray-400",
                        ),
                        rx.el.p(
                            DashboardState.system_load.to_string() + "%",
                            class_name="text-xl font-bold text-gray-100",
                        ),
                        class_name="absolute top-5 right-5 bg-gray-800/70 p-2 rounded-md text-center border border-gray-700/50 backdrop-blur-sm",
                    ),
                    class_name="relative",
                ),
                rx.el.div(
                    rx.el.p(
                        "Content for " + DashboardState.active_performance_tab,
                        class_name="text-gray-400 p-10 text-center",
                    )
                ),
            )
        ),
        class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm mt-6",
    )


def main_content() -> rx.Component:
    return rx.el.main(
        rx.el.section(
            rx.el.div(
                rx.el.h2(
                    rx.icon(
                        tag="bar-chart-2",
                        class_name="mr-2 text-cyan-400 hidden sm:inline-block",
                    ),
                    "System Overview",
                    class_name="text-lg sm:text-xl font-semibold text-gray-200 flex items-center",
                ),
                rx.el.div(
                    rx.el.span(
                        "LIVE",
                        class_name="text-xs font-bold text-green-400 bg-green-900/50 px-2 py-1 rounded-full mr-2",
                    ),
                    rx.icon(
                        tag="refresh-cw",
                        class_name="text-gray-400 hover:text-gray-200 cursor-pointer",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.foreach(DashboardState.stat_cards, stat_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
            ),
            class_name="mb-6",
        ),
        rx.el.section(performance_section()),
        class_name="p-4 sm:p-6 flex-1 overflow-y-auto",
    )
