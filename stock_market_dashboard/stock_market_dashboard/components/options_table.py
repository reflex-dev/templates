import reflex as rx

from stock_market_dashboard.states.trading_state import TradingState


def options_header(
    stock_symbol: str,
    price: rx.Var[float],
    change: rx.Var[float],
    change_percent: rx.Var[float],
) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            f"{stock_symbol}",
            class_name="text-sm font-bold text-white mr-2",
        ),
        rx.el.span(
            price.to_string(),
            class_name="text-sm font-semibold text-white mr-1",
        ),
        rx.el.span(
            change.to_string(),
            class_name=rx.cond(
                change >= 0,
                "text-green-400 text-xs",
                "text-red-400 text-xs",
            ),
        ),
        rx.el.span(
            change_percent.to_string(),
            class_name=rx.cond(
                change >= 0,
                "text-green-400 text-xs ml-1",
                "text-red-400 text-xs ml-1",
            ),
        ),
        class_name="mb-2 px-2",
    )


def options_sub_tabs() -> rx.Component:
    tabs = [
        "4D Fri Oct 18",
        "11D Fri Oct 25",
        "18D Fri Nov 1",
        "25D Fri Nov 8",
        "32D Fri Nov 15",
    ]
    return rx.el.div(
        rx.foreach(
            tabs,
            lambda tab: rx.el.button(
                tab,
                on_click=TradingState.set_active_sub_tab(tab),
                class_name=rx.cond(
                    TradingState.active_sub_tab == tab,
                    "text-xs text-white bg-gray-700 px-3 py-1 rounded",
                    "text-xs text-gray-400 hover:text-white px-3 py-1",
                ),
            ),
        ),
        class_name="flex space-x-2 border-b border-gray-700 mb-2 pb-1 px-2 overflow-x-auto",
    )


def render_option_cell(
    value: rx.Var,
    class_name: str,
    is_numeric: bool = True,
    format_spec: str = ".2f",
    prefix: str = "",
    suffix: str = "",
) -> rx.Component:
    formatted_value = rx.cond(value, value.to_string(), "-")
    return rx.el.td(formatted_value, class_name=class_name)


def render_combined_option_row(
    item: rx.Var[dict[str, dict[str, int]]],
) -> rx.Component:
    call_option = item["call"]
    put_option = item["put"]
    strike = item["strike"]
    call_headers_config = [
        ("mark", "px-2 py-1 text-xs text-right"),
        (
            "percent_change_to",
            "px-2 py-1 text-xs text-right",
            True,
            ".2f",
            "",
            "%",
        ),
        (
            "delta",
            "px-2 py-1 text-xs text-right",
            True,
            ".4f",
        ),
        (
            "oi",
            "px-2 py-1 text-xs text-right text-gray-400",
            False,
        ),
        (
            "volume",
            "px-2 py-1 text-xs text-right text-gray-400",
            False,
        ),
        (
            "iv",
            "px-2 py-1 text-xs text-right",
            True,
            ".2f",
            "",
            "%",
        ),
        (
            "low",
            "px-2 py-1 text-xs text-right text-gray-400",
        ),
        (
            "high",
            "px-2 py-1 text-xs text-right text-gray-400",
        ),
        (
            "bid",
            rx.cond(
                call_option["bid"].to(int) > 0.5,
                "px-2 py-1 text-xs text-right font-semibold text-green-400",
                "px-2 py-1 text-xs text-right font-semibold text-red-400",
            ),
            True,
            ".2f",
            "$",
        ),
        (
            "ask",
            rx.cond(
                call_option["ask"] > 0.5,
                "px-2 py-1 text-xs text-right font-semibold text-green-400",
                "px-2 py-1 text-xs text-right font-semibold text-red-400",
            ),
            True,
            ".2f",
            "$",
        ),
    ]
    put_headers_config = [
        (
            "bid",
            rx.cond(
                put_option["bid"] > 0.5,
                "px-2 py-1 text-xs text-left font-semibold text-green-400",
                "px-2 py-1 text-xs text-left font-semibold text-red-400",
            ),
            True,
            ".2f",
            "$",
        ),
        (
            "ask",
            rx.cond(
                put_option["ask"] > 0.5,
                "px-2 py-1 text-xs text-left font-semibold text-green-400",
                "px-2 py-1 text-xs text-left font-semibold text-red-400",
            ),
            True,
            ".2f",
            "$",
        ),
        (
            "delta",
            "px-2 py-1 text-xs text-left",
            True,
            ".4f",
        ),
        (
            "oi",
            "px-2 py-1 text-xs text-left text-gray-400",
            False,
        ),
        (
            "volume",
            "px-2 py-1 text-xs text-left text-gray-400",
            False,
        ),
        (
            "iv",
            "px-2 py-1 text-xs text-left",
            True,
            ".2f",
            "",
            "%",
        ),
        (
            "percent_change_to",
            "px-2 py-1 text-xs text-left",
            True,
            ".2f",
            "",
            "%",
        ),
        ("mark", "px-2 py-1 text-xs text-left"),
        (
            "gamma",
            "px-2 py-1 text-xs text-left text-gray-400",
            True,
            ".2f",
        ),
    ]
    is_near_the_money = rx.Var.create(
        f"Math.abs({strike} - {TradingState.stock_info['price']}) < 5"
    )
    return rx.el.tr(
        rx.cond(
            call_option,
            rx.fragment(
                *[
                    render_option_cell(call_option[key], cn, *fmt)
                    for key, cn, *fmt in call_headers_config
                ]
            ),
            rx.fragment(
                *[
                    rx.el.td(
                        "-",
                        class_name="px-2 py-1 text-xs text-gray-500 text-right",
                    )
                    for _ in call_headers_config
                ]
            ),
        ),
        rx.el.td(
            strike.to_string(),
            class_name=rx.cond(
                is_near_the_money,
                "px-3 py-1 text-xs text-center font-bold text-white bg-yellow-700",
                "px-3 py-1 text-xs text-center font-bold text-white bg-gray-600",
            ),
        ),
        rx.cond(
            put_option,
            rx.fragment(
                *[
                    render_option_cell(put_option[key], cn, *fmt)
                    for key, cn, *fmt in put_headers_config
                ]
            ),
            rx.fragment(
                *[
                    rx.el.td(
                        "-",
                        class_name="px-2 py-1 text-xs text-gray-500 text-left",
                    )
                    for _ in put_headers_config
                ]
            ),
        ),
        class_name="border-b border-gray-700 hover:bg-gray-700",
    )


def options_table() -> rx.Component:
    call_headers = [
        "Mark",
        "% to",
        "Delta",
        "OI",
        "Volume",
        "IV",
        "Low",
        "High",
        "Bid",
        "Ask",
    ]
    put_headers = [
        "Bid",
        "Ask",
        "Delta",
        "OI",
        "Volume",
        "IV",
        "Change % to",
        "Mark",
        "Gamma",
    ]
    return rx.el.div(
        options_header(
            TradingState.stock_info["symbol"],
            TradingState.stock_info["price"],
            TradingState.stock_info["change"],
            TradingState.stock_info["change_percent"],
        ),
        options_sub_tabs(),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Calls",
                            col_span=len(call_headers),
                            class_name="text-sm font-semibold text-white pb-2 text-center border-b-2 border-green-500 sticky top-0 bg-gray-800 z-20",
                        ),
                        rx.el.th(
                            "Strike",
                            class_name="text-sm font-semibold text-white pb-2 text-center border-b-2 border-gray-500 sticky top-0 bg-gray-800 z-20",
                        ),
                        rx.el.th(
                            "Puts",
                            col_span=len(put_headers),
                            class_name="text-sm font-semibold text-white pb-2 text-center border-b-2 border-red-500 sticky top-0 bg-gray-800 z-20",
                        ),
                    ),
                    rx.el.tr(
                        rx.foreach(
                            call_headers,
                            lambda header: rx.el.th(
                                header,
                                class_name="px-2 py-1 text-xs font-normal text-gray-400 text-right sticky top-8 bg-gray-800 z-10",
                            ),
                        ),
                        rx.el.th(
                            "",
                            class_name="sticky top-8 bg-gray-800 z-10",
                        ),
                        rx.foreach(
                            put_headers,
                            lambda header: rx.el.th(
                                header,
                                class_name="px-2 py-1 text-xs font-normal text-gray-400 text-left sticky top-8 bg-gray-800 z-10",
                            ),
                        ),
                        class_name="border-b border-gray-700",
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(
                        TradingState.combined_options,
                        render_combined_option_row,
                    )
                ),
                class_name="w-full border-collapse text-gray-300 text-xs",
            ),
            class_name="overflow-y-auto h-full",
        ),
        class_name="bg-gray-800 p-3 rounded-lg border border-gray-700 flex-grow lg:col-span-2",
    )
