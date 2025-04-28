import reflex as rx

from stock_market_dashboard.states.trading_state import Order, TradingState


def get_status_color(status: rx.Var[str]) -> rx.Var[str]:
    return rx.match(
        status,
        ("Filled", "text-green-400"),
        ("Canceled", "text-red-400"),
        ("Working", "text-yellow-400"),
        ("Sending", "text-blue-400"),
        "text-gray-400",
    )


def get_side_color(side: rx.Var[str]) -> rx.Var[str]:
    return rx.cond(side == "Buy", "text-green-400", "text-red-400")


def render_order_row(order: Order) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            order["symbol"],
            class_name="px-3 py-2 whitespace-nowrap text-sm font-medium text-white",
        ),
        rx.el.td(
            order["status"],
            class_name=rx.cond(
                order["status"] == "Filled",
                "px-3 py-2 whitespace-nowrap text-sm text-green-400",
                rx.cond(
                    order["status"] == "Canceled",
                    "px-3 py-2 whitespace-nowrap text-sm text-red-400",
                    rx.cond(
                        order["status"] == "Working",
                        "px-3 py-2 whitespace-nowrap text-sm text-yellow-400",
                        rx.cond(
                            order["status"] == "Sending",
                            "px-3 py-2 whitespace-nowrap text-sm text-blue-400",
                            "px-3 py-2 whitespace-nowrap text-sm text-gray-400",
                        ),
                    ),
                ),
            ),
        ),
        rx.el.td(
            order["side"],
            class_name=rx.cond(
                order["side"] == "Buy",
                "px-3 py-2 whitespace-nowrap text-sm text-green-400",
                "px-3 py-2 whitespace-nowrap text-sm text-red-400",
            ),
        ),
        rx.el.td(
            order["type"],
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300",
        ),
        rx.el.td(
            order["qty"].to_string(),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-right",
        ),
        rx.el.td(
            order["total_cost"].to_string(),
            class_name="px-3 py-2 whitespace-nowrap text-sm text-gray-300 text-right",
        ),
        class_name="border-b border-gray-700 hover:bg-gray-700",
    )


def orders_table() -> rx.Component:
    headers = [
        "Symbol",
        "Status",
        "Side",
        "Type",
        "Qty",
        "Total cost",
    ]
    header_classes = [
        "px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase tracking-wider border-b border-gray-700",
        "px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase tracking-wider border-b border-gray-700",
        "px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase tracking-wider border-b border-gray-700",
        "px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase tracking-wider border-b border-gray-700",
        "px-3 py-2 text-right text-xs font-medium text-gray-400 uppercase tracking-wider border-b border-gray-700",
        "px-3 py-2 text-right text-xs font-medium text-gray-400 uppercase tracking-wider border-b border-gray-700",
    ]
    return rx.el.div(
        rx.el.h3(
            "Recent orders",
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
                        TradingState.recent_orders,
                        render_order_row,
                    )
                ),
                class_name="min-w-full divide-y divide-gray-700",
            ),
            class_name="overflow-y-auto max-h-[200px]",
        ),
        class_name="bg-gray-800 p-3 rounded-lg border border-gray-700 lg:col-span-2",
    )
