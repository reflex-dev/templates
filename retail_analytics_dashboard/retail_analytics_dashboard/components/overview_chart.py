from typing import List

import reflex as rx

from retail_analytics_dashboard.models.models import ChartDataPoint, OverviewMetric
from retail_analytics_dashboard.states.data import TOOLTIP_PROPS


def overview_chart(
    metric: rx.Var[OverviewMetric],
) -> rx.Component:
    """Renders a single overview metric card with a small chart."""
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                metric["title"],
                class_name="text-sm text-gray-600",
            ),
            rx.el.span(
                metric["change"],
                class_name="ml-2 text-xs font-medium px-1.5 py-0.5 rounded-full "
                + rx.cond(
                    metric["change_color"] == "text-green-600",
                    "bg-green-100 text-green-600",
                    "bg-red-100 text-red-600",
                ),
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.p(
                metric["value"],
                class_name="text-2xl font-semibold text-gray-900 mt-1",
            ),
            rx.el.p(
                metric["previous_value"],
                class_name="text-xs text-gray-500",
            ),
            class_name="flex items-end justify-between align-end",
        ),
        rx.el.div(
            rx.recharts.line_chart(
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    class_name="opacity-50",
                ),
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.recharts.line(
                    data_key="value1",
                    stroke="#8884d8",
                    stroke_width=2,
                    dot=False,
                    type_="monotone",
                ),
                rx.recharts.line(
                    data_key="value2",
                    stroke="#cccccc",
                    stroke_width=2,
                    dot=False,
                    type_="monotone",
                ),
                rx.recharts.x_axis(
                    data_key="date",
                    hide=True,
                    axis_line=False,
                    tick_line=False,
                ),
                rx.recharts.y_axis(
                    hide=True,
                    axis_line=False,
                    tick_line=False,
                    domain=["auto", "auto"],
                ),
                data=metric["chart_data"].to(List[ChartDataPoint]),
                height=120,
                margin={
                    "top": 5,
                    "right": 5,
                    "left": 5,
                    "bottom": 5,
                },
                class_name="[&_.recharts-tooltip-item-unit]:text-gray-600 [&_.recharts-tooltip-item-unit]:font-mono [&_.recharts-tooltip-item-value]:!text-gray-900 [&_.recharts-tooltip-item-value]:!font-mono [&_.recharts-tooltip-item-value]:mr-[0.2rem] [&_.recharts-tooltip-item]:flex [&_.recharts-tooltip-item]:items-center [&_.recharts-tooltip-item]:before:content-[''] [&_.recharts-tooltip-item]:before:size-2.5 [&_.recharts-tooltip-item]:before:rounded-[2px] [&_.recharts-tooltip-item]:before:shrink-0 [&_.recharts-tooltip-item]:before:!bg-[currentColor] [&_.recharts-tooltip-item-name]:text-gray-600 [&_.recharts-tooltip-item-list]:flex [&_.recharts-tooltip-item-list]:flex-col [&_.recharts-tooltip-item-name]:pr-[3rem] [&_.recharts-tooltip-item-name]:pl-1.5 [&_.recharts-tooltip-item-separator]:w-full [&_.recharts-tooltip-wrapper]:z-[1]",
            ),
            class_name="mt-3 -mb-2 -ml-2 -mr-2",
        ),
        class_name="p-4",
    )
