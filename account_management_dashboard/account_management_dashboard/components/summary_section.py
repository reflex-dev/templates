import reflex as rx

from account_management_dashboard.states.account_state import (
    AccountState,
    AssetLiabilitySummaryItem,
)


def summary_bar(item: AssetLiabilitySummaryItem, total: rx.Var[float]) -> rx.Component:
    """Creates a segment of the summary bar."""
    percentage = rx.cond(total == 0, 0, item["value"] / total * 100)
    return rx.el.div(
        class_name=f"{item['color']} h-2",
        style={"width": percentage.to_string() + "%"},
    )


def summary_list_item(
    item: AssetLiabilitySummaryItem,
    is_percent: rx.Var[bool],
) -> rx.Component:
    """Displays a single item in the summary list."""
    display_value = rx.cond(
        is_percent,
        item["value"].to_string() + "%",
        "$" + item["value"].to_string(),
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name=f"{item['color']} w-2.5 h-2.5 rounded-full mr-3"),
            rx.el.span(
                item["name"],
                class_name="text-sm text-gray-700",
            ),
            class_name="flex items-center",
        ),
        rx.el.span(
            display_value,
            class_name="text-sm font-medium text-gray-900",
        ),
        class_name="flex items-center justify-between py-1.5",
    )


def summary_section() -> rx.Component:
    """Displays the Assets and Liabilities summary."""
    is_totals_view = AccountState.summary_view == "Totals"
    is_percent_view = AccountState.summary_view == "Percent"
    assets_data = rx.cond(
        is_percent_view,
        AccountState.asset_percentages,
        AccountState.assets_summary,
    )
    liabilities_data = rx.cond(
        is_percent_view,
        AccountState.liability_percentages,
        AccountState.liabilities_summary,
    )
    total_assets_display = rx.cond(
        is_percent_view,
        "100.0%",
        "$" + AccountState.total_assets.to_string(),
    )
    total_liabilities_display = rx.cond(
        is_percent_view,
        "100.0%",
        "$" + AccountState.total_liabilities.to_string(),
    )
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Summary",
                class_name="text-lg font-semibold text-gray-900",
            ),
            rx.el.div(
                rx.el.button(
                    "Totals",
                    on_click=lambda: AccountState.set_summary_view("Totals"),
                    class_name=rx.cond(
                        is_totals_view,
                        "px-3 py-1 text-sm font-medium text-indigo-700 bg-indigo-100 rounded-md",
                        "px-3 py-1 text-sm font-medium text-gray-500 hover:text-gray-700",
                    ),
                ),
                rx.el.button(
                    "Percent",
                    on_click=lambda: AccountState.set_summary_view("Percent"),
                    class_name=rx.cond(
                        is_percent_view,
                        "px-3 py-1 text-sm font-medium text-indigo-700 bg-indigo-100 rounded-md",
                        "px-3 py-1 text-sm font-medium text-gray-500 hover:text-gray-700",
                    ),
                ),
                class_name="flex space-x-1 bg-gray-100 p-0.5 rounded-lg",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h4(
                    "Assets",
                    class_name="text-sm font-medium text-gray-500",
                ),
                rx.el.span(
                    total_assets_display,
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="flex items-center justify-between mb-2",
            ),
            rx.el.div(
                rx.foreach(
                    AccountState.assets_summary,
                    lambda item: summary_bar(item, AccountState.total_assets),
                ),
                class_name="flex w-full h-2 bg-gray-200 rounded-full overflow-hidden mb-3",
            ),
            rx.el.div(
                rx.foreach(
                    assets_data,
                    lambda item: summary_list_item(item, is_percent_view),
                ),
                class_name="space-y-1",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h4(
                    "Liabilities",
                    class_name="text-sm font-medium text-gray-500",
                ),
                rx.el.span(
                    total_liabilities_display,
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="flex items-center justify-between mb-2",
            ),
            rx.el.div(
                rx.foreach(
                    AccountState.liabilities_summary,
                    lambda item: summary_bar(item, AccountState.total_liabilities),
                ),
                class_name="flex w-full h-2 bg-gray-200 rounded-full overflow-hidden mb-3",
            ),
            rx.el.div(
                rx.foreach(
                    liabilities_data,
                    lambda item: summary_list_item(item, is_percent_view),
                ),
                class_name="space-y-1",
            ),
        ),
        class_name="p-6 bg-white border border-gray-200 rounded-lg shadow-sm",
    )
