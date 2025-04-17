import reflex as rx
from stock_market_dashboard.states.trading_state import TradingState


def main_header() -> rx.Component:
    tabs = [
        "Options trading",
        "Market tracker",
        "Positions analysis",
    ]
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.img(
                    src="/favicon.ico",
                    class_name="h-6 w-6 mr-4",
                ),
                rx.foreach(
                    tabs,
                    lambda tab: rx.el.button(
                        tab,
                        on_click=TradingState.set_active_main_tab(
                            tab
                        ),
                        class_name=rx.cond(
                            TradingState.active_main_tab
                            == tab,
                            "px-3 py-2 text-sm font-medium text-white border-b-2 border-green-500",
                            "px-3 py-2 text-sm font-medium text-gray-400 hover:text-white hover:border-b-2 hover:border-gray-500",
                        ),
                    ),
                ),
                rx.el.button(
                    "+",
                    class_name="ml-2 px-2 py-1 text-sm font-medium text-gray-400 hover:text-white hover:bg-gray-700 rounded",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "▲ 0.39% Today",
                        class_name="text-xs bg-green-900 text-green-300 px-2 py-1 rounded-full mr-4",
                    )
                ),
                rx.el.button(
                    "Add widget",
                    class_name="bg-gray-700 hover:bg-gray-600 text-white text-xs font-semibold py-1 px-3 rounded mr-4",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option(
                            "Individual", value="individual"
                        ),
                        default_value="individual",
                        class_name="bg-gray-700 text-white text-xs rounded border-0 focus:ring-0 mr-3 py-1",
                    ),
                    rx.el.img(
                        src="/favicon.ico",
                        class_name="h-6 w-6 rounded-full",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-center w-full",
        ),
        class_name="bg-gray-900 text-gray-300 px-4 py-2 border-b border-gray-700",
    )