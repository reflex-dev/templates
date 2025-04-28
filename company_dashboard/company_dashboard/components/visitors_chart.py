import reflex as rx

from company_dashboard.states.dashboard_state import (
    TOOLTIP_PROPS,
    DashboardState,
)


def time_range_button(text: str) -> rx.Component:
    """Button for selecting chart time range."""
    return rx.el.button(
        text,
        on_click=lambda: DashboardState.set_visitor_timeframe(text),
        class_name=rx.cond(
            DashboardState.selected_visitor_timeframe == text,
            "px-3 py-1 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md shadow-sm",
            "px-3 py-1 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50",
        ),
    )


def visitors_chart_section() -> rx.Component:
    """The section displaying the total visitors chart."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Total Visitors",
                    class_name="text-lg font-semibold text-gray-900",
                ),
                rx.el.p(
                    "Total for the last 3 months",
                    class_name="text-sm text-gray-500",
                ),
            ),
            rx.el.div(
                time_range_button("Last 3 months"),
                time_range_button("Last 30 days"),
                time_range_button("Last 7 days"),
                class_name="flex items-center space-x-2",
            ),
            class_name="flex flex-wrap items-center justify-between mb-4 gap-y-2",
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                vertical=False,
                stroke="#e5e7eb",
            ),
            rx.recharts.graphing_tooltip(
                content_style=TOOLTIP_PROPS["content_style"],
                item_style=TOOLTIP_PROPS["item_style"],
                label_style=TOOLTIP_PROPS["label_style"],
                cursor={
                    "stroke": "#d1d5db",
                    "strokeWidth": 1,
                },
            ),
            rx.recharts.x_axis(
                data_key="date",
                tick_line=False,
                axis_line=False,
                tick_margin=10,
                tick_count=10,
                interval="preserveStartEnd",
                tick_size=5,
                height=40,
                custom_attrs={"fontSize": "12px"},
                min_tick_gap=16,
            ),
            rx.recharts.y_axis(hide=True, domain=["auto", "auto"]),
            rx.recharts.area(
                data_key="series1",
                type_="natural",
                stroke="#f97316",
                fill="url(#colorSeries1)",
                stroke_width=1,
                dot=False,
                active_dot={
                    "r": 4,
                    "fill": "#f97316",
                    "stroke": "white",
                    "strokeWidth": 2,
                },
            ),
            rx.recharts.area(
                data_key="series2",
                type_="natural",
                stroke="#14b8a6",
                fill="url(#colorSeries2)",
                stroke_width=2,
                dot=False,
                active_dot={
                    "r": 4,
                    "fill": "#14b8a6",
                    "stroke": "white",
                    "strokeWidth": 2,
                },
            ),
            rx.el.defs(
                rx.el.linear_gradient(
                    rx.el.stop(
                        offset="5%",
                        stop_color="#f97316",
                        stop_opacity=0.3,
                    ),
                    rx.el.stop(
                        offset="95%",
                        stop_color="#f97316",
                        stop_opacity=0,
                    ),
                    id="colorSeries1",
                    x1="0",
                    y1="0",
                    x2="0",
                    y2="1",
                ),
                rx.el.linear_gradient(
                    rx.el.stop(
                        offset="5%",
                        stop_color="#14b8a6",
                        stop_opacity=0.3,
                    ),
                    rx.el.stop(
                        offset="95%",
                        stop_color="#14b8a6",
                        stop_opacity=0,
                    ),
                    id="colorSeries2",
                    x1="0",
                    y1="0",
                    x2="0",
                    y2="1",
                ),
            ),
            data=DashboardState.displayed_visitor_data,
            height=360,
            margin={
                "top": 25,
                "right": 0,
                "left": 0,
                "bottom": 0,
            },
        ),
        class_name="p-5 bg-white border border-gray-200 rounded-lg shadow-sm mt-5",
    )
