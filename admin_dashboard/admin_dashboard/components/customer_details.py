import reflex as rx
import reflex.components.recharts as recharts

from admin_dashboard.states.dashboard_state import (
    CustomerData,
    DashboardState,
)


def detail_item(label: str, value: rx.Var[str]) -> rx.Component:
    """Displays a single detail item with label and value."""
    return rx.el.div(
        rx.el.dt(
            label,
            class_name="text-sm font-medium text-gray-500",
        ),
        rx.el.dd(value, class_name="mt-1 text-sm text-gray-900"),
        class_name="py-2",
    )


def license_stat(label: str, value: rx.Var[int], change: rx.Var[int]) -> rx.Component:
    """Displays a license statistic card."""
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-sm font-medium text-gray-500",
        ),
        rx.el.div(
            rx.el.span(
                value,
                class_name="text-3xl font-bold text-gray-900 mr-2",
            ),
            rx.el.span(
                rx.icon(
                    rx.cond(change > 0, "arrow-up", "arrow-down"),
                    size=16,
                    class_name="mr-1",
                ),
                rx.cond(change < 0, change * -1, change),
                "%",
                class_name=rx.cond(
                    change > 0,
                    "text-sm font-medium text-green-600 bg-green-100 px-2 py-0.5 rounded-full inline-flex items-center",
                    "text-sm font-medium text-red-600 bg-red-100 px-2 py-0.5 rounded-full inline-flex items-center",
                ),
            ),
            class_name="flex items-baseline",
        ),
        class_name="p-4 bg-white rounded-lg border border-gray-200 shadow-sm",
    )


def customer_details_panel(
    customer: CustomerData,
) -> rx.Component:
    """Panel showing detailed information about a selected customer."""
    usage_percentage = rx.cond(
        customer["licenses"] > 0,
        round(customer["active_licenses"] * 100 / customer["licenses"]).to(int),
        0,
    )
    return rx.el.div(
        rx.el.h3(
            customer["customer_name"],
            class_name="text-xl font-semibold text-gray-900 mb-4",
        ),
        rx.el.div(
            rx.el.h4(
                "Usage",
                class_name="text-md font-medium text-gray-700 mb-2",
            ),
            rx.el.div(
                rx.el.p(
                    usage_percentage.to_string() + "%",
                    class_name="text-5xl font-bold text-emerald-600 text-center",
                ),
                class_name="flex items-center justify-center w-32 h-32 rounded-full bg-emerald-50 border-4 border-emerald-200 mx-auto mb-4",
            ),
            class_name="mb-6 p-4 bg-white rounded-lg border border-gray-200 shadow-sm",
        ),
        rx.el.div(
            rx.el.h4(
                "Details",
                class_name="text-md font-medium text-gray-700 mb-2",
            ),
            rx.el.dl(
                detail_item(
                    "Revenue",
                    "$" + customer["revenue"].to_string(),
                ),
                detail_item("Platform Type", customer["platform"]),
                detail_item("Industry", customer["industry"]),
            ),
            class_name="mb-6 p-4 bg-white rounded-lg border border-gray-200 divide-y divide-gray-200 shadow-sm",
        ),
        rx.el.div(
            rx.el.h4(
                "License Utilization",
                class_name="text-md font-medium text-gray-700 mb-3",
            ),
            rx.el.div(
                license_stat(
                    "Active Licenses",
                    customer["active_licenses"],
                    customer["active_license_growth"],
                ),
                license_stat(
                    "Total Licenses",
                    customer["licenses"],
                    customer["license_growth"],
                ),
                class_name="grid grid-cols-2 gap-4 mb-4",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.h4(
                "Usage Over Time",
                class_name="text-md font-medium text-gray-700 mb-2",
            ),
            rx.el.div(
                recharts.line_chart(
                    recharts.cartesian_grid(
                        horizontal=True,
                        vertical=False,
                        class_name="opacity-25 stroke-gray-300",
                    ),
                    recharts.line(
                        data_key="usage",
                        stroke="#10B981",
                        stroke_width=2,
                        dot=False,
                        type_="natural",
                    ),
                    recharts.x_axis(
                        data_key="month",
                        axis_line=False,
                        tick_size=10,
                        tick_line=False,
                        interval="preserveStartEnd",
                    ),
                    recharts.y_axis(
                        axis_line=False,
                        tick_size=0,
                        tick_line=False,
                        width=30,
                    ),
                    data=customer["usage_history"],
                    height=250,
                    margin={
                        "top": 5,
                        "right": 10,
                        "left": 0,
                        "bottom": 5,
                    },
                ),
                class_name="p-2 bg-white rounded-lg border border-gray-200 flex items-center justify-center shadow-sm",
            ),
        ),
        class_name="px-5 pt-5 pb-14 bg-gray-50 rounded-lg shadow-inner h-[100vh] overflow-y-auto",
    )


def customer_details() -> rx.Component:
    """Component to display details of the selected customer or a placeholder."""
    return rx.el.div(
        rx.cond(
            DashboardState.selected_customer,
            customer_details_panel(DashboardState.selected_customer),
            rx.el.div(
                rx.el.p(
                    "Select a customer to see details.",
                    class_name="text-center text-gray-500 text-lg",
                ),
                class_name="flex items-center justify-center h-[100vh] p-5 bg-gray-50 rounded-lg shadow-inner",
            ),
        ),
        class_name="col-span-1",
    )
