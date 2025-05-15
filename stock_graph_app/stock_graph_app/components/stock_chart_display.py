import reflex as rx

from stock_graph_app.states.stock_state import StockState

TOOLTIP_PROPS = {
    "content_style": {
        "background": "#2d2e30",
        "borderColor": "#2d2e3065",
        "borderRadius": "0.75rem",
        "boxShadow": "0px 24px 12px 0px light-dark(rgba(28, 32, 36, 0.02), rgba(0, 0, 0, 0.00)), 0px 8px 8px 0px light-dark(rgba(28, 32, 36, 0.02), rgba(0, 0, 0, 0.00)), 0px 2px 6px 0px light-dark(rgba(28, 32, 36, 0.02), rgba(0, 0, 0, 0.00))",
        "fontFamily": "sans-serif",
        "fontSize": "0.875rem",
        "lineHeight": "1.25rem",
        "fontWeight": "500",
        "minWidth": "8rem",
        "padding": "0.375rem 0.625rem",
        "position": "relative",
    },
    "item_style": {
        "display": "flex",
        "paddingBottom": "0px",
        "position": "relative",
        "paddingTop": "2px",
    },
    "label_style": {
        "color": "#d4d4d4",
        "fontWeight": "500",
        "alignSelf": "flex-end",
    },
    "separator": "",
}


def live_indicator_dot() -> rx.Component:
    """Creates a pulsing green dot to indicate live market activity."""
    return rx.el.span(
        rx.el.span(
            class_name="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"
        ),
        rx.el.span(class_name="relative inline-flex rounded-full h-2 w-2 bg-green-500"),
        class_name="relative flex h-2 w-2",
    )


def search_bar_component() -> rx.Component:
    return rx.el.form(
        rx.el.input(
            name="ticker_input",
            placeholder="Enter Ticker (e.g., AAPL, MSFT)",
            class_name="bg-[#2d2e30] text-white placeholder-neutral-400 border border-neutral-600 rounded-lg p-2 text-sm w-full sm:flex-grow focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none transition-shadow shadow-sm hover:shadow-md focus:shadow-lg",
        ),
        rx.el.button(
            "Get Data",
            type="submit",
            class_name="text-nowrap bg-emerald-600 hover:bg-emerald-700 text-white font-semibold p-2 text-sm rounded-lg transition-all duration-150 ease-in-out shadow hover:shadow-md active:bg-emerald-800 w-full sm:w-auto sm:px-3",
            is_loading=StockState.is_loading,
        ),
        on_submit=StockState.fetch_stock_data,
        reset_on_submit=False,
        class_name="mb-8 flex flex-col sm:flex-row items-stretch sm:items-center space-y-2 sm:space-y-0 sm:space-x-2",
    )


def stock_header_component() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    StockState.stock_ticker,
                    class_name="text-2xl sm:text-3xl md:text-4xl font-bold tracking-tight text-white",
                ),
                rx.el.div(
                    rx.cond(
                        StockState.logo_url != "",
                        rx.image(
                            src=StockState.logo_url,
                            alt=StockState.company_name,
                            height="24px",
                            width="24px",
                            class_name="mr-2 rounded-md self-center",
                            fallback="",
                        ),
                    ),
                    rx.el.p(
                        StockState.company_name,
                        class_name="text-sm sm:text-base text-neutral-300 self-center",
                    ),
                    class_name="flex items-center mt-1 sm:mt-1.5 mb-1",
                ),
                rx.el.p(
                    StockState.exchange_info,
                    class_name="text-xs text-neutral-500",
                ),
                class_name="flex-grow pb-3 w-full sm:w-auto",
            ),
            rx.el.div(
                rx.el.div(
                    rx.cond(
                        StockState.is_market_currently_active
                        & StockState.has_data_to_display,
                        rx.el.div(live_indicator_dot(), class_name="mr-2 self-center"),
                    ),
                    rx.el.span(StockState.current_price_display_val),
                    rx.el.span(
                        StockState.company_info.get("currency", ""),
                        class_name="text-neutral-400 text-base sm:text-lg ml-1 self-baseline",
                    ),
                    class_name="flex items-baseline text-2xl sm:text-3xl md:text-4xl font-bold text-white text-left sm:text-right",
                ),
                rx.el.p(
                    "Market Cap: ",
                    StockState.market_cap_display_val,
                    class_name="text-xs text-neutral-500 text-left sm:text-right mt-0.5",
                ),
                rx.el.p(
                    "At Regular Market Close",
                    class_name="text-xs text-neutral-500 text-left sm:text-right",
                ),
                class_name="text-left sm:text-right flex-shrink-0 w-full sm:w-auto mt-3 sm:mt-0 sm:ml-4 pb-3",
            ),
            class_name="flex flex-col sm:flex-row justify-between items-stretch sm:items-start mb-2 border-neutral-700",
        ),
        rx.cond(
            StockState.show_after_hours_section,
            rx.el.div(
                rx.el.p(
                    StockState.after_hours_price_display_val,
                    " ",
                    rx.el.span(
                        StockState.after_hours_change_display_val,
                        class_name="text-neutral-500 font-semibold",
                    ),
                    rx.el.span(
                        StockState.company_info.get("currency", ""),
                        class_name="text-neutral-400 text-xs sm:text-sm ml-1 self-baseline",
                    ),
                    class_name="text-base sm:text-lg md:text-xl font-semibold text-white text-left sm:text-right",
                ),
                rx.el.p(
                    StockState.after_hours_label,
                    class_name="text-xs text-neutral-500 text-left sm:text-right mt-0.5",
                ),
                class_name="mt-3 mb-1 w-full text-left sm:text-right",
            ),
        ),
        class_name="mb-5",
    )


def time_range_selector_component() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            StockState.time_ranges,
            lambda time_range: rx.el.button(
                time_range,
                on_click=lambda: StockState.set_time_range(time_range),
                class_name=rx.cond(
                    StockState.selected_time_range == time_range,
                    "bg-emerald-600 text-white font-semibold px-2.5 py-1.5 rounded-md text-xs sm:text-sm mx-0.5 sm:mx-1 my-1 min-w-[3rem] text-center shadow-md",
                    "bg-[#2d2e30] text-neutral-300 hover:bg-neutral-700 hover:text-white px-2.5 py-1.5 rounded-md text-xs sm:text-sm mx-0.5 sm:mx-1 my-1 min-w-[3rem] text-center transition-colors duration-150 ease-in-out shadow-sm hover:shadow-md",
                ),
                disabled=StockState.is_loading,
            ),
        ),
        class_name="flex flex-wrap justify-center md:justify-start items-center my-4 md:my-6 pb-3 sm:pb-4 border-neutral-700",
    )


def chart_component() -> rx.Component:
    gradient_id = "stockPriceGradient"
    return rx.el.div(
        rx.el.svg(
            rx.el.defs(
                rx.el.svg.linear_gradient(
                    rx.el.svg.stop(
                        offset="5%",
                        stop_color="#22C55E",
                        stop_opacity=0.4,
                    ),
                    rx.el.svg.stop(
                        offset="95%",
                        stop_color="#22C55E",
                        stop_opacity=0.05,
                    ),
                    id=gradient_id,
                    x1="0",
                    y1="0",
                    x2="0",
                    y2="1",
                )
            ),
            class_name="w-0 h-0 absolute",
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                horizontal=True,
                vertical=False,
                stroke_dasharray="3 3",
                stroke_opacity=0.2,
                stroke="#555555",
            ),
            rx.recharts.graphing_tooltip(
                **TOOLTIP_PROPS,
            ),
            rx.recharts.y_axis(
                orientation="left",
                data_key="price",
                domain=StockState.y_axis_domain,
                axis_line=False,
                tick_line=False,
                class_name="text-neutral-400 text-sm",
                label=StockState.y_axis_label_config,
            ),
            rx.recharts.x_axis(
                data_key="name",
                include_hidden=False,
                type_="category",
                tick_line=False,
                axis_line=False,
                tick_count=10,
                tick_size=16,
                tick_margin=8,
                min_tick_gap=32,
                interval="equidistantPreserveStart",
                class_name="text-neutral-400 text-xs",
            ),
            rx.recharts.area(
                data_key="price",
                name=StockState.currency_code,
                type_="monotone",
                stroke="#16A34A",
                fill=f"url(#{gradient_id})",
                stroke_width=2,
                dot=False,
                active_dot=True,
            ),
            data=StockState.current_stock_data_for_chart,
            height=350,
            margin={
                "top": 5,
                "right": 0,
                "left": 0,
                "bottom": 5,
            },
            class_name="w-full [&_.recharts-tooltip-item-unit]:text-neutral-100 [&_.recharts-tooltip-item-unit]:font-mono [&_.recharts-tooltip-item-value]:!text-neutral-100 [&_.recharts-tooltip-item-value]:!font-mono [&_.recharts-tooltip-item-value]:mr-[0.2rem] [&_.recharts-tooltip-item]:flex [&_.recharts-tooltip-item]:items-center [&_.recharts-tooltip-item]:before:content-[''] [&_.recharts-tooltip-item]:before:size-2.5 [&_.recharts-tooltip-item]:before:rounded-[2px] [&_.recharts-tooltip-item]:before:shrink-0 [&_.recharts-tooltip-item]:before:!bg-[currentColor] [&_.recharts-tooltip-item-name]:text-neutral-300 [&_.recharts-tooltip-item-list]:flex [&_.recharts-tooltip-item-list]:flex-col [&_.recharts-tooltip-item-name]:pr-[3rem] [&_.recharts-tooltip-item-name]:pl-1.5 [&_.recharts-tooltip-item-separator]:w-full [&_.recharts-tooltip-wrapper]:z-[1]",
        ),
        class_name="w-full h-[350px] mt-4",
    )


def loading_spinner_component() -> rx.Component:
    return rx.el.div(
        rx.spinner(class_name="text-green-500 w-12 h-12"),
        class_name="w-full h-[300px] flex justify-center items-center",
    )


def error_message_component() -> rx.Component:
    return rx.el.div(
        StockState.error_message,
        class_name="text-red-400 text-sm my-4 p-3 bg-red-900/40 border border-red-700/50 rounded-lg flex items-center shadow",
    )


def no_data_component() -> rx.Component:
    return rx.el.div(
        "No data to display. Please search for a stock ticker above or select a different time range.",
        class_name="w-full h-[300px] flex flex-col justify-center items-center text-neutral-500 text-center p-4",
    )


def stock_graph_page() -> rx.Component:
    return rx.el.div(
        search_bar_component(),
        rx.cond(StockState.error_message, error_message_component(), rx.el.div()),
        rx.cond(
            StockState.is_loading,
            loading_spinner_component(),
            rx.cond(
                StockState.has_data_to_display,
                rx.fragment(
                    stock_header_component(),
                    time_range_selector_component(),
                    chart_component(),
                ),
                rx.cond(~StockState.error_message, no_data_component(), rx.el.div()),
            ),
        ),
        rx.moment(
            interval=5000,
            on_change=StockState.refresh_data.temporal,
            class_name="hidden pointer-events-none",
        ),
        class_name="bg-gradient-to-br from-[#202123] to-[#2a2b2f] text-white p-3 sm:p-4 md:p-6 rounded-lg sm:rounded-xl shadow-xl sm:shadow-2xl w-full max-w-4xl mx-auto my-4 sm:my-8",
        on_mount=StockState.on_load_fetch,
    )
