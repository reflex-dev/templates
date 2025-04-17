from typing import Dict, List

import reflex as rx

from manufacturing_dashboard.states.dashboard_state import (
    DashboardState,
)


def sparkline_chart(
    data: rx.Var[List[Dict[str, int]]],
) -> rx.Component:
    """Renders a small sparkline chart for the metrics table."""
    return rx.recharts.line_chart(
        rx.recharts.line(
            data_key="uv",
            stroke="#fbbf24",
            stroke_width=2,
            dot=False,
            is_animation_active=False,
        ),
        data=data,
        width=120,
        height=40,
        margin={
            "top": 5,
            "right": 0,
            "left": 0,
            "bottom": 5,
        },
    )


def ooc_progress_bar(
    percentage: rx.Var[float],
) -> rx.Component:
    """Renders a segmented progress bar for OOC percentage.
    Teal: 0-3%, Amber: 3-7%, Red: 7-10%
    """
    teal_width = rx.cond(percentage <= 3, percentage * 100 / 3, 100).to_string() + "%"
    yellow_width = (
        rx.cond(
            percentage > 3,
            rx.cond(
                percentage <= 7,
                (percentage - 3) * 100 / 4,
                100,
            ),
            0,
        ).to_string()
        + "%"
    )
    red_width = (
        rx.cond(
            percentage > 7,
            rx.cond(
                percentage <= 10,
                (percentage - 7) * 100 / 3,
                100,
            ),
            0,
        ).to_string()
        + "%"
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                style={"width": teal_width},
                class_name="h-full bg-teal-500 rounded-l",
            ),
            class_name="w-1/3 h-full",
        ),
        rx.el.div(
            rx.el.div(
                style={"width": yellow_width},
                class_name="h-full bg-amber-400",
            ),
            class_name="w-1/3 h-full",
        ),
        rx.el.div(
            rx.el.div(
                style={"width": red_width},
                class_name="h-full bg-red-500 rounded-r",
            ),
            class_name="w-1/3 h-full",
        ),
        class_name="w-24 h-3 bg-slate-600 rounded flex overflow-hidden shadow-inner",
    )


def pass_fail_indicator(
    status: rx.Var[bool],
) -> rx.Component:
    """Renders a small colored dot indicating pass (amber) or fail (red)."""
    return rx.el.div(
        class_name=rx.cond(
            status,
            "w-3 h-3 rounded-full bg-amber-400 shadow-md",
            "w-3 h-3 rounded-full bg-red-500 shadow-md",
        )
    )


def metrics_summary() -> rx.Component:
    """Renders the main table for process control metrics."""
    headers = [
        "Parameter",
        "Count",
        "Trend",
        "OOC %",
        "% OOC Bar",
        "Status",
    ]
    return rx.el.div(
        rx.el.h2(
            "Process Control Metrics Summary",
            class_name="text-xl font-semibold text-slate-200 mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.foreach(
                            headers,
                            lambda header: rx.el.th(
                                header,
                                class_name="px-5 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider border-b border-slate-700 bg-slate-800",
                            ),
                        )
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.process_metrics,
                        lambda metric: rx.el.tr(
                            rx.el.td(
                                metric["parameter"],
                                class_name="px-5 py-4 whitespace-nowrap text-sm text-slate-300 border-b border-slate-700 font-medium",
                            ),
                            rx.el.td(
                                metric["count"],
                                class_name="px-5 py-4 whitespace-nowrap text-sm text-slate-300 border-b border-slate-700",
                            ),
                            rx.el.td(
                                sparkline_chart(metric["sparkline_data"]),
                                class_name="px-5 py-2 border-b border-slate-700",
                            ),
                            rx.el.td(
                                metric["ooc_percent"].to_string() + "%",
                                class_name="px-5 py-4 whitespace-nowrap text-sm text-slate-300 border-b border-slate-700 font-mono",
                            ),
                            rx.el.td(
                                ooc_progress_bar(metric["ooc_percent"]),
                                class_name="px-5 py-4 border-b border-slate-700",
                            ),
                            rx.el.td(
                                pass_fail_indicator(metric["pass_fail"]),
                                class_name="px-5 py-4 border-b border-slate-700",
                            ),
                            class_name="hover:bg-slate-700/50 transition-colors duration-150",
                        ),
                    )
                ),
                class_name="min-w-full",
            ),
            class_name="overflow-x-auto rounded-lg shadow-md border border-slate-700",
        ),
        class_name="bg-slate-800 p-6 rounded-lg shadow-lg border border-slate-700 w-full mb-6",
    )
