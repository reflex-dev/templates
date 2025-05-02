import reflex as rx
import reflex.components.recharts as recharts

from business_analytics_dashboard.components.tooltip_props import TOOLTIP_PROPS
from business_analytics_dashboard.states.dashboard_state import DashboardState


def department_pie_chart() -> rx.Component:
    """A pie chart showing the distribution of employees by department."""
    return rx.el.div(
        rx.el.h2(
            "Department Distribution",
            class_name="text-lg font-semibold text-gray-800 mb-4 text-center",
        ),
        rx.cond(
            DashboardState.loading,
            rx.el.p(
                "Loading chart data...",
                class_name="text-gray-500 text-center",
            ),
            rx.cond(
                DashboardState.department_distribution.length() > 0,
                recharts.pie_chart(
                    recharts.graphing_tooltip(**TOOLTIP_PROPS),
                    recharts.pie(
                        rx.foreach(
                            DashboardState.department_distribution,
                            lambda data_point, _: recharts.cell(
                                fill=DashboardState.department_color_map.get(
                                    data_point["name"],
                                    "#8884d8",
                                )
                            ),
                        ),
                        data=DashboardState.department_distribution,
                        data_key="value",
                        name_key="name",
                        cx="50%",
                        cy="50%",
                        outer_radius="80%",
                        padding_angle=5,
                        stroke="0",
                        label=True,
                        inner_radius=90,
                        custom_attrs={
                            "fontSize": "12px",
                            "fontWeight": "bold",
                            "paddingAngle": 3,
                            "cornerRadius": 5,
                        },
                    ),
                    recharts.legend(
                        height=36,
                        layout="horizontal",
                        vertical_align="bottom",
                        align="center",
                        icon_size=10,
                        icon_type="square",
                    ),
                    width="100%",
                    height=350,
                    class_name="[&_.recharts-tooltip-item-separator]:w-full",
                ),
                rx.el.p(
                    rx.cond(
                        (DashboardState.selected_department != "All")
                        | (DashboardState.search_query != ""),
                        rx.cond(
                            DashboardState.search_query != "",
                            "No employee data matches your search criteria.",
                            f"No employee data available for the '{DashboardState.selected_department}' department.",
                        ),
                        "No employee data available to display the chart.",
                    ),
                    class_name="text-gray-500 text-center py-10",
                ),
            ),
        ),
        class_name="bg-white p-6 rounded-lg h-auto min-h-[32rem]",
    )
