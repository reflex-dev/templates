import reflex as rx

from account_management_dashboard.states.account_state import AccountState


def net_worth_summary() -> rx.Component:
    """Displays the net worth and its change."""
    change_color = rx.cond(
        AccountState.net_worth_change_amount >= 0,
        "text-green-600",
        "text-red-600",
    )
    change_icon = rx.cond(
        AccountState.net_worth_change_amount >= 0,
        "arrow_up",
        "arrow_down",
    )
    change_sign = rx.cond(AccountState.net_worth_change_amount >= 0, "+", "")
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                "NET WORTH",
                class_name="text-xs font-medium text-gray-500 uppercase tracking-wider mr-2",
            ),
            rx.icon(
                tag="info",
                size=14,
                class_name="text-gray-400 cursor-pointer",
            ),
            class_name="flex items-center mb-1",
        ),
        rx.el.div(
            rx.el.span(
                "$",
                AccountState.net_worth.to_string(),
                class_name="text-3xl font-bold text-gray-900 mr-3",
            ),
            rx.el.div(
                rx.icon(
                    tag=change_icon,
                    size=16,
                    class_name=f"mr-1 {change_color}",
                ),
                rx.el.span(
                    change_sign,
                    "$",
                    AccountState.net_worth_change_amount.to_string(),
                    f" ({AccountState.net_worth_change_percent.to_string()}%)",
                    class_name=f"text-sm font-medium {change_color}",
                ),
                rx.el.span(
                    " 1 month change",
                    class_name="text-sm text-gray-500 ml-1",
                ),
                class_name="flex items-center",
            ),
            class_name="flex flex-wrap items-baseline gap-y-2",
        ),
        class_name="mb-6",
    )
