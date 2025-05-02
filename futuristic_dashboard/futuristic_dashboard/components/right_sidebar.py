import reflex as rx

from futuristic_dashboard.states.dashboard_state import (
    DashboardState,
    QuickActionData,
    ResourceAllocationData,
)


def system_time_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "SYSTEM TIME",
            class_name="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3",
        ),
        rx.el.p(
            DashboardState.current_time,
            class_name="text-3xl sm:text-4xl font-light text-cyan-300 tracking-widest mb-1",
        ),
        rx.el.p(
            DashboardState.current_date,
            class_name="text-sm text-gray-400 mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Uptime",
                    class_name="text-xs text-gray-500 mb-1",
                ),
                rx.el.p(
                    DashboardState.uptime,
                    class_name="text-xs sm:text-sm font-medium text-gray-200",
                ),
                class_name="bg-gray-700/50 p-2 sm:p-3 rounded-lg text-center",
            ),
            rx.el.div(
                rx.el.p(
                    "Time Zone",
                    class_name="text-xs text-gray-500 mb-1",
                ),
                rx.el.p(
                    DashboardState.time_zone,
                    class_name="text-xs sm:text-sm font-medium text-gray-200",
                ),
                class_name="bg-gray-700/50 p-2 sm:p-3 rounded-lg text-center",
            ),
            class_name="grid grid-cols-2 gap-2 sm:gap-3",
        ),
        class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm mb-6",
    )


def quick_action_button(
    action: QuickActionData,
) -> rx.Component:
    return rx.el.button(
        rx.icon(
            tag=action["icon"],
            class_name="size-5 mb-1 sm:mb-2",
        ),
        rx.el.span(action["name"], class_name="text-xs"),
        class_name="flex flex-col items-center justify-center bg-gray-700/50 p-3 sm:p-4 rounded-lg text-gray-300 hover:bg-gray-700 hover:text-cyan-300 transition-colors duration-150 focus:outline-none focus:ring-1 focus:ring-cyan-500 aspect-square",
    )


def quick_actions_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Quick Actions",
            class_name="text-sm sm:text-base font-semibold text-gray-300 mb-3",
        ),
        rx.el.div(
            rx.foreach(
                DashboardState.quick_actions,
                quick_action_button,
            ),
            class_name="grid grid-cols-2 gap-2 sm:gap-3",
        ),
        class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm mb-6",
    )


def resource_allocation_item(
    resource: ResourceAllocationData,
) -> rx.Component:
    value_str = resource["value"].to_string()
    color = resource["color"]
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                resource["name"],
                class_name="text-xs sm:text-sm font-medium text-gray-300",
            ),
            rx.el.span(
                value_str + "% allocated",
                class_name=rx.cond(
                    color == "cyan",
                    "text-xs sm:text-sm font-medium text-cyan-400",
                    rx.cond(
                        color == "pink",
                        "text-xs sm:text-sm font-medium text-pink-400",
                        rx.cond(
                            color == "blue",
                            "text-xs sm:text-sm font-medium text-blue-400",
                            "text-xs sm:text-sm font-medium text-gray-400",
                        ),
                    ),
                ),
            ),
            class_name="flex justify-between mb-1",
        ),
        rx.el.div(
            rx.el.div(
                style={"width": value_str + "%"},
                class_name=rx.cond(
                    color == "cyan",
                    "h-1.5 rounded-full bg-cyan-500",
                    rx.cond(
                        color == "pink",
                        "h-1.5 rounded-full bg-pink-500",
                        rx.cond(
                            color == "blue",
                            "h-1.5 rounded-full bg-blue-500",
                            "h-1.5 rounded-full bg-gray-500",
                        ),
                    ),
                ),
            ),
            class_name="w-full bg-gray-700 rounded-full h-1.5",
        ),
        class_name="mb-3 sm:mb-4",
    )


def resource_allocation_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Resource Allocation",
            class_name="text-sm sm:text-base font-semibold text-gray-300 mb-3",
        ),
        rx.foreach(
            DashboardState.resource_allocation,
            resource_allocation_item,
        ),
        class_name="bg-gray-800/50 border border-gray-700/50 rounded-xl p-4 shadow-md backdrop-blur-sm",
    )


def right_sidebar() -> rx.Component:
    return rx.el.aside(
        system_time_section(),
        resource_allocation_section(),
        class_name="w-72 px-4 pt-4 pb-10 sm:p-6 flex-shrink-0 overflow-y-auto hidden lg:block h-screen sticky top-0 right-0",
    )
