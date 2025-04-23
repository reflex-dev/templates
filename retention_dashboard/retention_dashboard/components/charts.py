from typing import Dict, List, Union

import reflex as rx

TooltipPropValue = Union[str, int, float, dict, bool]
TOOLTIP_PROPS: Dict[str, Dict[str, TooltipPropValue]] = {
    "content_style": {
        "background": "white",
        "borderColor": "#E8E8E8",
        "borderRadius": "0.75rem",
        "boxShadow": "0px 24px 12px 0px rgba(28, 32, 36, 0.02), 0px 8px 8px 0px rgba(28, 32, 36, 0.02), 0px 2px 6px 0px rgba(28, 32, 36, 0.02)",
        "fontFamily": "sans-serif",
        "fontSize": "0.875rem",
        "lineHeight": "1.25rem",
        "fontWeight": "500",
        "minWidth": "8rem",
        "padding": "0.375rem 0.625rem",
    },
    "item_style": {
        "display": "flex",
        "paddingBottom": "0px",
        "position": "relative",
        "paddingTop": "2px",
    },
    "label_style": {
        "color": "black",
        "fontWeight": "500",
        "alignSelf": "flex-end",
    },
    "separator": "",
}
ChartDataItem = Dict[str, Union[str, int, float]]


def donut_chart(
    data: rx.Var[List[ChartDataItem]],
    data_key: str,
    name_key: str,
    title: str,
    total_value: rx.Var[int],
    percentage: rx.Var[float],
) -> rx.Component:
    """Creates a reusable donut chart component."""
    return rx.el.div(
        rx.el.p(
            title,
            class_name="text-sm font-medium text-gray-600 text-center mb-2",
        ),
        rx.el.div(
            rx.recharts.pie_chart(
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.recharts.pie(
                    rx.recharts.cell(fill=rx.Var.create(f"{data[0]['fill']}")),
                    data=data,
                    data_key=data_key,
                    name_key=name_key,
                    cx="50%",
                    cy="50%",
                    inner_radius="70%",
                    outer_radius="100%",
                    padding_angle=0,
                    stroke="none",
                ),
                width="100%",
                height=150,
                class_name="relative [&_.recharts-tooltip-item-unit]:text-gray-600 [&_.recharts-tooltip-item-unit]:font-mono [&_.recharts-tooltip-item-value]:!text-gray-900 [&_.recharts-tooltip-item-value]:!font-mono [&_.recharts-tooltip-item-value]:mr-[0.2rem] [&_.recharts-tooltip-item]:flex [&_.recharts-tooltip-item]:items-center [&_.recharts-tooltip-item]:before:content-[''] [&_.recharts-tooltip-item]:before:size-2.5 [&_.recharts-tooltip-item]:before:rounded-[2px] [&_.recharts-tooltip-item]:before:shrink-0 [&_.recharts-tooltip-item]:before:!bg-[currentColor] [&_.recharts-tooltip-item-name]:text-gray-600 [&_.recharts-tooltip-item-list]:flex [&_.recharts-tooltip-item-list]:flex-col [&_.recharts-tooltip-item-name]:pr-[3rem] [&_.recharts-tooltip-item-name]:pl-1.5 [&_.recharts-tooltip-item-separator]:w-full [&_.recharts-tooltip-wrapper]:z-[1]",
            ),
            rx.el.div(
                rx.el.p(
                    total_value.to_string(),
                    class_name="text-xl font-bold text-gray-800",
                ),
                rx.el.p(
                    percentage.to_string() + "%",
                    class_name="text-xs text-gray-500",
                ),
                class_name="absolute inset-0 flex flex-col items-center justify-center pointer-events-none",
            ),
            class_name="relative",
        ),
        class_name="flex flex-col items-center",
    )
