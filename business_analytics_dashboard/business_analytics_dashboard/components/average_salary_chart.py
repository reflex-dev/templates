import reflex as rx
import reflex.components.recharts as recharts

from business_analytics_dashboard.components.tooltip_props import TOOLTIP_PROPS
from business_analytics_dashboard.states.dashboard_state import DashboardState


def average_salary_bar_chart() -> rx.Component:
    """A bar chart showing the average salary per department."""
    return rx.el.div(
        rx.el.h2(
            "Average Salary by Department",
            class_name="text-lg font-semibold text-gray-800 mb-4 text-center",
        ),
        rx.cond(
            DashboardState.loading,
            rx.el.p(
                "Loading chart data...",
                class_name="text-gray-500 text-center",
            ),
            rx.cond(
                DashboardState.average_salary_by_department.length() > 0,
                recharts.bar_chart(
                    recharts.graphing_tooltip(**TOOLTIP_PROPS),
                    recharts.cartesian_grid(
                        horizontal=True,
                        vertical=False,
                        class_name="opacity-25",
                        stroke=rx.color("gray", 7),
                    ),
                    recharts.bar(
                        rx.foreach(
                            DashboardState.average_salary_by_department,
                            lambda data_point, index: recharts.cell(
                                fill=DashboardState.department_color_map.get(
                                    data_point["department"],
                                    "#8884d8",
                                )
                            ),
                        ),
                        data_key="average_salary",
                        name="Average Salary",
                        radius=5,
                        bar_size=30,
                    ),
                    recharts.x_axis(
                        data_key="department",
                        type_="category",
                        tick_line=False,
                        axis_line=False,
                        height=50,
                        custom_attrs={"fontSize": "12px"},
                        stroke=rx.color("gray", 9),
                        interval=0,
                        angle=-45,
                        text_anchor="end",
                    ),
                    recharts.y_axis(
                        tick_line=False,
                        axis_line=False,
                        custom_attrs={"fontSize": "12px"},
                        stroke=rx.color("gray", 9),
                        tick_formatter="function(value) { return `$${value.toLocaleString()}`; }",
                    ),
                    data=DashboardState.average_salary_by_department,
                    height=350,
                    width="100%",
                    margin={
                        "left": 30,
                        "right": 30,
                        "top": 20,
                        "bottom": 30,
                    },
                    class_name="mt-4",
                ),
                rx.el.p(
                    rx.cond(
                        DashboardState.selected_department != "All",
                        f"No salary data available for the '{DashboardState.selected_department}' department.",
                        "No salary data available to display the chart.",
                    ),
                    class_name="text-gray-500 text-center py-10",
                ),
            ),
        ),
        class_name="bg-white p-6 rounded-lg h-auto min-h-[24rem]",
    )
