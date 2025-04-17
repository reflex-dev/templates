import reflex as rx
from account_management_dashboard.states.account_state import AccountState

try:
    import reflex.components.recharts as recharts

    recharts_available = True
except ImportError:
    recharts_available = False


def graph_placeholder() -> rx.Component:
    return rx.el.div(
        "Graph component requires 'recharts'. Please install it.",
        class_name="p-10 text-center bg-gray-100 border border-gray-300 rounded-lg text-red-600",
    )


def net_worth_graph_component() -> rx.Component:
    """Displays the net worth performance graph."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.select(
                    rx.el.option(
                        AccountState.selected_performance_type,
                        value=AccountState.selected_performance_type,
                    ),
                    value=AccountState.selected_performance_type,
                    class_name="text-sm border border-gray-300 rounded-md px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 cursor-not-allowed opacity-70",
                    disabled=True,
                ),
                rx.el.select(
                    rx.foreach(
                        AccountState.graph_ranges,
                        lambda range_option: rx.el.option(
                            range_option, value=range_option
                        ),
                    ),
                    value=AccountState.selected_graph_range,
                    on_change=AccountState.set_graph_range,
                    class_name="text-sm border border-gray-300 rounded-md px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500",
                ),
                class_name="flex space-x-3 mb-4",
            ),
            rx.cond(
                recharts_available,
                recharts.line_chart(
                    recharts.line(
                        data_key="value",
                        type="monotone",
                        stroke="#2563eb",
                        stroke_width=2,
                        dot=False,
                        active_dot={
                            "r": 6,
                            "fill": "#2563eb",
                            "stroke": "#fff",
                            "strokeWidth": 2,
                        },
                    ),
                    recharts.x_axis(
                        data_key="date",
                        tick_line=False,
                        axis_line=False,
                        font_size=12,
                        stroke="#9ca3af",
                    ),
                    recharts.y_axis(
                        axis_line=False,
                        tick_line=False,
                        domain=[
                            "dataMin - 1000",
                            "dataMax + 1000",
                        ],
                        allow_decimals=False,
                        font_size=12,
                        stroke="#9ca3af",
                    ),
                    rx.recharts.tooltip(
                        content_style={
                            "backgroundColor": "#ffffff",
                            "borderColor": "#e5e7eb",
                            "borderRadius": "0.375rem",
                            "boxShadow": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                        },
                        label_style={
                            "color": "#1f2937",
                            "fontWeight": "500",
                        },
                        item_style={"color": "#4b5563"},
                        formatter="function(value) { return '$' + value.toLocaleString(); }",
                    ),
                    recharts.cartesian_grid(
                        stroke_dasharray="3 3",
                        stroke="#e5e7eb",
                    ),
                    data=AccountState.net_worth_performance_data,
                    height=250,
                    margin={
                        "top": 5,
                        "right": 5,
                        "left": 15,
                        "bottom": 5,
                    },
                ),
                graph_placeholder(),
            ),
            class_name="p-4 bg-white border border-gray-200 rounded-lg shadow-sm",
        ),
        class_name="mb-8",
    )
