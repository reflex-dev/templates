from typing import Dict, List, Union

import reflex as rx

from marketing_dashboard.states.marketing_dashboard_state import (
    TOOLTIP_PROPS,
)


def kpi_section(
    title: str,
    value: Union[str, int, rx.Var],
    description: str,
) -> rx.Component:
    """Simplified KPI section for the top part of the chart card."""
    return rx.el.div(
        rx.el.p(
            title,
            class_name="text-sm font-medium text-gray-400 uppercase tracking-wider",
        ),
        rx.el.p(
            value,
            class_name="text-4xl sm:text-5xl font-bold text-white mt-2",
        ),
        rx.el.p(
            description,
            class_name="text-base text-gray-300 mt-1",
        ),
    )


def line_chart_card(
    title: str,
    data: rx.Var[List[Dict[str, Union[str, int]]]],
    y_max: int,
    kpi_value: Union[str, int, rx.Var],
    kpi_desc: str,
) -> rx.Component:
    """A card containing a line chart and related KPI."""
    return rx.el.div(
        kpi_section(title, kpi_value, kpi_desc),
        rx.el.div(
            rx.recharts.line_chart(
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    class_name="stroke-gray-700 opacity-50",
                ),
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.recharts.line(
                    data_key="past_28_days",
                    stroke="#00BFFF",
                    dot=False,
                    type_="monotone",
                    stroke_width=2,
                    connect_nulls=True,
                ),
                rx.recharts.line(
                    data_key="prev_28_days",
                    stroke="#FFD700",
                    dot=False,
                    type_="monotone",
                    stroke_width=2,
                    connect_nulls=True,
                ),
                rx.recharts.y_axis(
                    domain=[0, y_max],
                    axis_line=False,
                    tick_line=False,
                    tick_size=10,
                    tick_formatter="(value) => value.toLocaleString()",
                    custom_attrs={
                        "fontSize": "12px",
                        "stroke": "#A0AEC0",
                    },
                    width=40,
                ),
                rx.recharts.x_axis(
                    data_key="date",
                    axis_line=False,
                    tick_line=False,
                    tick_size=10,
                    custom_attrs={
                        "fontSize": "12px",
                        "stroke": "#A0AEC0",
                    },
                    interval=6,
                    padding={"left": 10, "right": 10},
                ),
                rx.recharts.legend(
                    payload=[
                        {
                            "value": "past 28 days",
                            "type": "circle",
                            "id": "past_28_days",
                            "color": "#00BFFF",
                        },
                        {
                            "value": "prev 28 days",
                            "type": "circle",
                            "id": "prev_28_days",
                            "color": "#FFD700",
                        },
                    ],
                    icon_size=8,
                    wrapper_style={
                        "paddingTop": "20px",
                        "color": "#A0AEC0",
                        "fontSize": "12px",
                    },
                    align="right",
                    vertical_align="top",
                ),
                data=data,
                height=200,
                margin={
                    "top": 5,
                    "right": 10,
                    "left": -25,
                    "bottom": 5,
                },
            ),
            class_name="mt-4",
        ),
        class_name="bg-indigo-900 p-4 sm:p-6 rounded-lg shadow-lg",
    )
