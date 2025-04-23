from typing import Union

import reflex as rx

from stock_market_dashboard.states.trading_state import Position, TradingState


def format_currency(
    value: rx.Var[Union[float, None]],
) -> rx.Var[str]:
    return rx.cond(value is not None, value.to_string(), "-")


def format_signed_currency(
    value: rx.Var[Union[float, None]],
) -> rx.Var[str]:
    return rx.cond(value is not None, value.to_string(), "-")


def format_float(
    value: rx.Var[Union[float, None]],
    format_spec: str = ".2f",
) -> rx.Var[str]:
    return rx.cond(value is not None, value.to_string(), "-")


def format_signed_percent(
    value: rx.Var[Union[float, None]],
) -> rx.Var[str]:
    return rx.cond(value is not None, value.to_string(), "-")


def get_return_color(
    value: rx.Var[Union[float, None]],
) -> rx.Var[str]:
    return rx.cond(
        value is not None,
        rx.cond(value >= 0, "text-green-400", "text-red-400"),
        "text-gray-300",
    )


def render_position_row(pos: Position) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            pos["symbol"],
            class_name="px-3 py-2 whitespace-nowrap text-sm font-medium text-white",
        ),
        rx.el.td(
            format_float(pos["qty"], ".3f"),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-right",
        ),
        rx.el.td(
            format_currency(pos["mkt_val"]),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-right",
        ),
        rx.el.td(
            format_signed_currency(pos["day_return"]),
            class_name=rx.cond(
                pos["day_return"] is not None,
                rx.cond(
                    pos["day_return"] >= 0,
                    "px-3 py-2 whitespace-nowrap text-sm text-right text-green-400",
                    "px-3 py-2 whitespace-nowrap text-sm text-right text-red-400",
                ),
                "px-3 py-2 whitespace-nowrap text-sm text-right text-gray-300",
            ),
        ),
        rx.el.td(
            format_signed_percent(pos["day_percent"]),
            class_name=rx.cond(
                pos["day_percent"] is not None,
                rx.cond(
                    pos["day_percent"] >= 0,
                    "px-3 py-2 whitespace-nowrap text-sm text-right text-green-400",
                    "px-3 py-2 whitespace-nowrap text-sm text-right text-red-400",
                ),
                "px-3 py-2 whitespace-nowrap text-sm text-right text-gray-300",
            ),
        ),
        rx.el.td(
            format_currency(pos["total_ret"]),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-right",
        ),
        rx.el.td(
            format_float(pos["mark"]),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-right",
        ),
        rx.el.td(
            format_float(pos["avg_cost"]),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-right",
        ),
        rx.el.td(
            format_float(pos["bid"]),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-right",
        ),
        rx.el.td(
            format_float(pos["ask"]),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-right",
        ),
        rx.el.td(
            format_float(pos["delta"], ".4f"),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-right",
        ),
        rx.el.td(
            format_float(pos["gamma"], ".4f"),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-right",
        ),
        rx.el.td(
            format_float(pos["theta"], ".4f"),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-right",
        ),
        rx.el.td(
            rx.cond(
                pos["iv"] is not None,
                format_float(pos["iv"].to(float), ".2f") + "%",
                "-",
            ),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-right",
        ),
        rx.el.td(
            pos["type"],
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300",
        ),
        rx.el.td(
            pos["dte"].to_string(),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-center",
        ),
        class_name="border-b border-gray-700 hover:bg-gray-700",
    )


def positions_table() -> rx.Component:
    headers = [
        "Symbol",
        "Qty",
        "Mkt val",
        "Day return",
        "Day %",
        "Total ret",
        "Mark",
        "Avg cost",
        "Bid",
        "Ask",
        "Delta",
        "Gamma",
        "Theta",
        "IV",
        "Type",
        "DTE",
    ]
    header_alignments = [
        "left",
        "right",
        "right",
        "right",
        "right",
        "right",
        "right",
        "right",
        "right",
        "right",
        "right",
        "right",
        "right",
        "right",
        "left",
        "center",
    ]
    header_classes = [
        f"px-3 py-2 text-{align} text-xs font-medium text-gray-400 uppercase tracking-wider border-b border-gray-700 whitespace-nowrap"
        for align in header_alignments
    ]
    return rx.el.div(
        rx.el.h3(
            "Positions",
            class_name="text-lg font-semibold text-white mb-3 px-3",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.foreach(
                            list(zip(headers, header_classes)),
                            lambda item: rx.el.th(item[0], class_name=item[1]),
                        ),
                        class_name="sticky top-0 bg-gray-800 z-10",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        TradingState.positions,
                        render_position_row,
                    )
                ),
                class_name="min-w-full divide-y divide-gray-700",
            ),
            class_name="overflow-x-auto overflow-y-auto max-h-[200px]",
        ),
        class_name="bg-gray-800 p-3 rounded-lg border border-gray-700",
    )
