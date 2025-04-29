from typing import Dict, List

import reflex as rx

from futuristic_dashboard.states.dashboard_state import (
    PerformanceChartData,
)

TOOLTIP_PROPS = {
    "cursor": {"fill": "rgba(200, 200, 200, 0.1)"},
    "content_style": {
        "backgroundColor": "rgba(30, 41, 59, 0.9)",
        "borderColor": "rgba(51, 65, 85, 0.5)",
        "borderRadius": "8px",
        "boxShadow": "0 2px 10px rgba(0,0,0,0.2)",
        "padding": "8px 12px",
    },
    "label_style": {
        "color": "#cbd5e1",
        "fontSize": "12px",
        "fontWeight": "bold",
    },
    "item_style": {"color": "#94a3b8", "fontSize": "12px"},
}
RECHART_WRAPPER_CLASS = "[&_.recharts-tooltip-cursor]:fill-zinc-500/10 [&_.recharts-tooltip-item]:!text-gray-300 [&_.recharts-tooltip-item-name]:!text-gray-400 [&_.recharts-tooltip-item-separator]:!text-gray-400 [&_.recharts-label]:!fill-gray-400 [&_.recharts-cartesian-axis-tick-value]:!fill-gray-400 [&_.recharts-legend-item-text]:!text-gray-300"


def stat_card_chart(
    data: rx.Var[List[Dict[str, int]]], color: rx.Var[str]
) -> rx.Component:
    return rx.recharts.area_chart(
        rx.recharts.area(
            data_key="v",
            type_="natural",
            fill=rx.match(
                color,
                ("cyan", "url(#cyanGradient)"),
                ("purple", "url(#purpleGradient)"),
                ("teal", "url(#tealGradient)"),
                "url(#defaultGradient)",
            ),
            stroke=rx.match(
                color,
                ("cyan", "#22d3ee"),
                ("purple", "#a855f7"),
                ("teal", "#2dd4bf"),
                "#8884d8",
            ),
            stroke_width=2,
            dot=False,
            fill_opacity=0.3,
        ),
        rx.el.defs(
            rx.el.linear_gradient(
                rx.el.stop(
                    offset="5%",
                    stop_color="#22d3ee",
                    stop_opacity=0.8,
                ),
                rx.el.stop(
                    offset="95%",
                    stop_color="#22d3ee",
                    stop_opacity=0,
                ),
                id="cyanGradient",
                x1="0",
                y1="0",
                x2="0",
                y2="1",
            ),
            rx.el.linear_gradient(
                rx.el.stop(
                    offset="5%",
                    stop_color="#a855f7",
                    stop_opacity=0.8,
                ),
                rx.el.stop(
                    offset="95%",
                    stop_color="#a855f7",
                    stop_opacity=0,
                ),
                id="purpleGradient",
                x1="0",
                y1="0",
                x2="0",
                y2="1",
            ),
            rx.el.linear_gradient(
                rx.el.stop(
                    offset="5%",
                    stop_color="#2dd4bf",
                    stop_opacity=0.8,
                ),
                rx.el.stop(
                    offset="95%",
                    stop_color="#2dd4bf",
                    stop_opacity=0,
                ),
                id="tealGradient",
                x1="0",
                y1="0",
                x2="0",
                y2="1",
            ),
            rx.el.linear_gradient(
                rx.el.stop(
                    offset="5%",
                    stop_color="#8884d8",
                    stop_opacity=0.8,
                ),
                rx.el.stop(
                    offset="95%",
                    stop_color="#8884d8",
                    stop_opacity=0,
                ),
                id="defaultGradient",
                x1="0",
                y1="0",
                x2="0",
                y2="1",
            ),
        ),
        data=data,
        width="100%",
        height=50,
        margin={
            "top": 5,
            "right": 0,
            "left": 0,
            "bottom": 0,
        },
    )


def performance_line_chart(
    data: rx.Var[List[PerformanceChartData]],
) -> rx.Component:
    return rx.recharts.line_chart(
        rx.recharts.cartesian_grid(
            stroke_dasharray="3 3",
            stroke="#374151",
            vertical=False,
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.x_axis(
            data_key="time",
            axis_line=False,
            tick_line=False,
            tick_margin=10,
            style={"fontSize": "12px"},
        ),
        rx.recharts.y_axis(
            axis_line=False,
            tick_line=False,
            tick_margin=10,
            domain=[0, 100],
            style={"fontSize": "12px"},
        ),
        rx.recharts.line(
            data_key="CPU",
            type_="monotone",
            stroke="#22d3ee",
            stroke_width=2,
            dot=False,
            name="CPU",
        ),
        rx.recharts.line(
            data_key="Memory",
            type_="monotone",
            stroke="#a855f7",
            stroke_width=2,
            dot=False,
            name="Memory",
        ),
        rx.recharts.line(
            data_key="Network",
            type_="monotone",
            stroke="#14b8a6",
            stroke_width=2,
            dot=False,
            name="Network",
        ),
        rx.recharts.legend(
            icon_type="circle",
            icon_size=10,
            wrapper_style={"paddingTop": "20px"},
        ),
        data=data,
        width="100%",
        height=300,
        margin={
            "top": 5,
            "right": 20,
            "left": -10,
            "bottom": 5,
        },
        class_name=RECHART_WRAPPER_CLASS,
    )
