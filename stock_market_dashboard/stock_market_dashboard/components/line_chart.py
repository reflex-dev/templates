import reflex as rx

from stock_market_dashboard.components.tooltip_props import TOOLTIP_PROPS
from stock_market_dashboard.states.trading_state import StockInfo, TradingState


def stock_info_header(stock: StockInfo) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                stock["symbol"],
                class_name="text-xl font-bold text-white",
            ),
            rx.el.span(
                stock["price"].to_string(),
                class_name="text-xl font-semibold text-white mr-2",
            ),
            rx.el.span(
                stock["change"].to_string(),
                class_name=rx.cond(
                    stock["change"] >= 0,
                    "text-green-400",
                    "text-red-400",
                ),
            ),
            rx.el.span(
                stock["change_percent"].to_string(),
                class_name=rx.cond(
                    stock["change"] >= 0,
                    "text-green-400 text-sm ml-1",
                    "text-red-400 text-sm ml-1",
                ),
            ),
            class_name="flex items-baseline gap-2",
        ),
        rx.el.div(
            rx.el.button(
                "Buy",
                class_name="bg-green-500 hover:bg-green-600 text-white text-xs font-bold py-1 px-4 rounded mr-2",
            ),
            rx.el.button(
                "Sell",
                class_name="bg-red-500 hover:bg-red-600 text-white text-xs font-bold py-1 px-4 rounded",
            ),
            rx.el.div(
                rx.el.span(
                    stock["open"].to_string(),
                    class_name="text-xs text-gray-400 ml-4",
                ),
                rx.el.span(
                    stock["high"].to_string(),
                    class_name="text-xs text-gray-400 ml-2",
                ),
                rx.el.span(
                    stock["low"].to_string(),
                    class_name="text-xs text-gray-400 ml-2",
                ),
                rx.el.span(
                    stock["close"].to_string(),
                    class_name="text-xs text-gray-400 ml-2",
                ),
                rx.el.span(
                    f"V {stock['volume']}",
                    class_name="text-xs text-gray-400 ml-2",
                ),
                class_name="flex flex-row items-center max-md:hidden",
            ),
            class_name="flex flex-wrap items-center mt-1",
        ),
        class_name="mb-3",
    )


def chart_controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.foreach(
                ["1D", "1W", "1M", "3M", "1Y", "5Y", "All"],
                lambda item: rx.el.button(
                    item,
                    class_name="text-xs text-gray-400 hover:text-white px-2 py-1 rounded hover:bg-gray-700",
                ),
            ),
            class_name="flex space-x-1",
        ),
        rx.el.div(
            rx.el.span(
                "Interval: 1h",
                class_name="text-xs text-gray-400 mr-3",
            ),
            rx.el.button(
                "Auto-scale",
                class_name="text-xs text-gray-400 hover:text-white px-2 py-1 rounded hover:bg-gray-700",
            ),
            class_name="flex items-center",
        ),
        class_name="flex justify-between items-center mt-2 px-2 max-md:hidden",
    )


def trading_line_chart() -> rx.Component:
    min_price = rx.Var.create(
        f"Math.min(...{TradingState.chart_data.to_string()}.map(p => p.price))"
    ).to(int)
    max_price = rx.Var.create(
        f"Math.max(...{TradingState.chart_data.to_string()}.map(p => p.price))"
    ).to(int)
    padding = (max_price - min_price) * 0.1
    y_domain = rx.Var.create(f"[{min_price} - {padding}, {max_price} + {padding}]")
    return rx.el.div(
        stock_info_header(TradingState.stock_info),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                stroke="#4b5563",
                horizontal=True,
                vertical=False,
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.line(
                data_key="price",
                stroke="#22c55e",
                dot=False,
                type_="monotone",
                stroke_width=2,
                is_animation_active=False,
            ),
            rx.recharts.x_axis(
                data_key="time",
                axis_line=False,
                tick_line=False,
                stroke="#9ca3af",
                tick_size=10,
                tick_count=6,
                interval="preserveStartEnd",
                padding={"left": 10, "right": 10},
                custom_attrs={"fontSize": "10px"},
            ),
            rx.recharts.y_axis(
                domain=y_domain,
                axis_line=False,
                tick_line=False,
                stroke="#9ca3af",
                orientation="right",
                tick_formatter="function(value) { return `$${value.toFixed(2)}`; }",
                width=55,
                allow_decimals=True,
                custom_attrs={"fontSize": "10px"},
            ),
            data=TradingState.chart_data,
            margin={
                "top": 5,
                "right": 0,
                "left": 0,
                "bottom": 5,
            },
            height=250,
            width="100%",
        ),
        chart_controls(),
        class_name="bg-gray-800 p-4 rounded-lg border border-gray-700 flex-grow lg:col-span-1",
    )
