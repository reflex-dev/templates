from typing import List

import reflex as rx

from account_management_dashboard.models.models import (
    AccountCategory,
    AccountDetail,
    SparklinePoint,
)
from account_management_dashboard.states.account_state import AccountState

try:
    import reflex.components.recharts as recharts

    recharts_available = True
except ImportError:
    recharts_available = False


def mini_sparkline(
    data_var: rx.Var[List[SparklinePoint]],
) -> rx.Component:
    """A small sparkline for account rows."""
    placeholder = rx.el.div(
        "~",
        class_name="text-gray-400 text-xs w-[80px] text-center",
    )
    return rx.cond(
        recharts_available & (data_var.length() > 0),
        recharts.line_chart(
            recharts.line(
                data_key="value",
                type="monotone",
                stroke="#6b7280",
                stroke_width=1,
                dot=False,
            ),
            recharts.y_axis(hide=True, domain=["dataMin", "dataMax"]),
            recharts.x_axis(hide=True),
            data=data_var,
            width=80,
            height=30,
            margin={
                "top": 5,
                "right": 0,
                "left": 0,
                "bottom": 5,
            },
        ),
        placeholder,
    )


def account_row(account: rx.Var[AccountDetail], index: rx.Var[int]) -> rx.Component:
    """Displays a single account row within a category."""
    return rx.el.div(
        rx.el.div(
            rx.el.img(
                src=rx.cond(
                    account["logo_url"],
                    account["logo_url"],
                    "/favicon.ico",
                ),
                class_name="w-8 h-8 mr-4 rounded-full border border-gray-200 object-contain",
            ),
            rx.el.div(
                rx.el.p(
                    account["name"],
                    class_name="text-sm font-medium text-gray-900",
                ),
                rx.el.p(
                    account["type"],
                    class_name="text-xs text-gray-500",
                ),
                class_name="flex-grow",
            ),
            class_name="flex items-center flex-grow",
        ),
        rx.el.div(
            mini_sparkline(account["sparkline_data"]),
            class_name="hidden md:block mx-4",
        ),
        rx.el.div(
            rx.el.p(
                "$" + account["balance"].to_string(),
                class_name="text-sm font-semibold text-gray-900 text-right",
            ),
            rx.el.p(
                account["last_updated"],
                class_name="text-xs text-gray-500 text-right",
            ),
            class_name="w-32 text-right ml-4",
        ),
        class_name="flex items-center justify-between py-3 px-4 hover:bg-gray-50 transition-colors duration-150 border-tb border-gray-100",
    )


def account_category_section(
    category: rx.Var[AccountCategory], index: rx.Var[int]
) -> rx.Component:
    """Displays a collapsible section for an account category."""
    is_open = category["is_open"]
    change_icon = rx.cond(
        category["one_month_change"] >= 0,
        "arrow_up",
        "arrow_down",
    )
    change_sign = rx.cond(category["one_month_change"] >= 0, "+", "")
    chevron_icon = rx.cond(is_open, "chevron_up", "chevron_down")
    total_balance_str = rx.cond(
        category["total_balance"] >= 0,
        category["total_balance"],
        category["total_balance"] * -1,
    )
    one_month_change_str = rx.cond(
        category["one_month_change"] >= 0,
        "$" + category["one_month_change"].to_string(),
        "-$" + (category["one_month_change"] * -1).to_string(),
    )
    one_month_change_percent_str = (
        category["one_month_change_percent"].to_string() + "%"
    )
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.icon(
                    tag=chevron_icon,
                    size=20,
                    class_name="text-gray-500 mr-3",
                ),
                rx.el.span(
                    category["category_name"],
                    class_name="text-sm font-semibold text-gray-800 mr-4",
                ),
                rx.icon(
                    tag=change_icon,
                    size=14,
                    class_name=rx.cond(
                        category["one_month_change"] >= 0,
                        "mr-1 text-green-600",
                        "mr-1 text-red-600",
                    ),
                ),
                rx.el.span(
                    change_sign,
                    one_month_change_str,
                    f" ({one_month_change_percent_str})",
                    class_name=rx.cond(
                        category["one_month_change"] >= 0,
                        "text-xs font-medium mr-2 text-green-600",
                        "text-xs font-medium mr-2 text-red-600",
                    ),
                ),
                rx.el.span(
                    "1 month change",
                    class_name="text-xs text-gray-500 hidden sm:inline",
                ),
                class_name="flex items-center flex-grow",
            ),
            rx.el.span(
                total_balance_str,
                class_name="text-sm font-semibold text-gray-900",
            ),
            on_click=lambda: AccountState.toggle_account_category(index),
            class_name=rx.cond(
                is_open,
                "flex items-center justify-between w-full px-4 py-3 bg-white hover:bg-gray-50 transition-colors duration-150 rounded-t-lg border border-b-0 border-gray-200",
                "flex items-center justify-between w-full px-4 py-3 bg-white hover:bg-gray-50 transition-colors duration-150 rounded-lg border border-b border-gray-200",
            ),
            # class_name=
        ),
        rx.cond(
            is_open,
            rx.el.div(
                rx.foreach(category["accounts"], account_row),
                class_name="bg-white border border-t-0 border-gray-200 rounded-b-lg overflow-hidden",
            ),
            None,
        ),
        class_name="mb-4",
    )
