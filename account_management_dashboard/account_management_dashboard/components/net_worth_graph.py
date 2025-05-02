import reflex as rx

from account_management_dashboard.states.account_state import AccountState

try:
    import reflex.components.recharts as recharts

    recharts_available = True
except ImportError:
    recharts_available = False
TOOLTIP_PROPS = {
    "content_style": {
        "backgroundColor": "#ffffff",
        "borderColor": "#e5e7eb",
        "borderRadius": "0.375rem",
        "boxShadow": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
        "fontFamily": "inherit",
        "fontSize": "0.875rem",
        "lineHeight": "1.25rem",
        "fontWeight": "500",
        "minWidth": "8rem",
        "padding": "0.5rem 0.75rem",
    },
    "item_style": {"padding": "0.125rem 0"},
    "label_style": {
        "color": "#6b7280",
        "fontSize": "0.75rem",
        "marginBottom": "0.25rem",
    },
    "formatter": "function(value) { return '$' + value.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}); }",
    "separator": ": ",
    "cursor": {"stroke": "#a0aec0", "strokeWidth": 1},
}


def graph_placeholder() -> rx.Component:
    """Placeholder shown if recharts is not available."""
    return rx.el.div(
        rx.el.p("Graph component requires the 'recharts' extra."),
        rx.el.p("Please install it using:"),
        rx.el.code("pip install reflex[recharts]"),
        class_name="p-10 text-center bg-gray-100 border border-gray-300 rounded-lg text-red-600 space-y-2",
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
                    default_value=AccountState.selected_performance_type,
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
                class_name="flex flex-wrap space-x-3 mb-4 gap-y-2",
            ),
            rx.cond(
                recharts_available,
                recharts.line_chart(
                    recharts.graphing_tooltip(**TOOLTIP_PROPS),
                    recharts.cartesian_grid(
                        stroke_dasharray="3 3",
                        stroke="#e5e7eb",
                        horizontal=True,
                        vertical=False,
                    ),
                    recharts.line(
                        data_key="value",
                        type_="monotone",
                        stroke="#2563eb",
                        stroke_width=2,
                        dot=False,
                        active_dot={
                            "r": 6,
                            "fill": "#2563eb",
                            "stroke": "#ffffff",
                            "strokeWidth": 2,
                        },
                        name="Net Worth",
                    ),
                    recharts.x_axis(
                        data_key="date",
                        axis_line=False,
                        tick_line=False,
                        min_tick_gap=20,
                        tick_margin=10,
                        tick_formatter="(value) => value",
                        padding={"left": 20, "right": 20},
                        stroke="#6b7280",
                        font_size=12,
                    ),
                    recharts.y_axis(
                        axis_line=False,
                        tick_line=False,
                        allow_decimals=True,
                        domain=["auto", "auto"],
                        tick_formatter="(value) => '$' + value.toLocaleString()",
                        width=80,
                        tick_margin=5,
                        stroke="#6b7280",
                        font_size=12,
                    ),
                    data=AccountState.net_worth_performance_data,
                    height=250,
                    width="100%",
                    margin={
                        "top": 5,
                        "right": 10,
                        "left": 10,
                        "bottom": 5,
                    },
                    class_name="[&_.recharts-tooltip-cursor]:stroke-gray-300",
                ),
                graph_placeholder(),
            ),
            class_name="p-4 bg-white border border-gray-200 rounded-lg shadow-sm",
        ),
        class_name="mb-8 w-full",
    )
