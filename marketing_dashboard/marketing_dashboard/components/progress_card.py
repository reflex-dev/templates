import reflex as rx
from typing import Union


def progress_card(
    title: str,
    budget_spent: Union[str, rx.Var],
    budget_total: Union[str, rx.Var],
    progress_value: Union[float, rx.Var],
    conversion_count: Union[int, rx.Var],
    cost_per_conversion: Union[str, rx.Var],
    show_warning_conv: bool = False,
) -> rx.Component:
    """A card for displaying budget progress and related conversion metrics."""
    return rx.el.div(
        rx.el.p(
            title,
            class_name="text-sm font-medium text-gray-400 uppercase tracking-wider",
        ),
        rx.el.p(
            budget_spent,
            class_name="text-3xl sm:text-4xl font-bold text-white mt-4",
        ),
        rx.el.p(
            "budget spent",
            class_name="text-sm text-gray-300 mt-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    style={"width": progress_value.to_string() + "%"},
                    class_name="bg-cyan-400 h-2 rounded-full transition-all duration-500",
                ),
                class_name="w-full bg-gray-700 rounded-full h-2 mt-3",
            ),
            rx.el.div(
                rx.el.span(
                    progress_value.to_string() + "%",
                    class_name="text-cyan-400",
                ),
                rx.el.span(budget_total, class_name="text-gray-400"),
                class_name="flex justify-between text-xs mt-1",
            ),
            class_name="w-full mt-2 mb-6",
        ),
        rx.el.div(
            rx.el.span(
                conversion_count,
                class_name="text-3xl sm:text-4xl font-bold text-white",
            ),
            rx.el.span(
                " conversions",
                class_name="text-sm text-gray-300 ml-2 align-bottom",
            ),
            class_name="mt-4",
        ),
        rx.el.div(
            rx.el.span(
                cost_per_conversion,
                class_name="text-3xl sm:text-4xl font-bold text-white",
            ),
            rx.el.span(
                " per conv",
                class_name="text-sm text-gray-300 ml-2 align-bottom",
            ),
            rx.cond(
                show_warning_conv,
                rx.el.div(
                    rx.el.span(
                        "!",
                        class_name="text-white font-bold text-xs",
                    ),
                    class_name="absolute -top-2 -right-2 bg-red-500 rounded-full w-5 h-5 flex items-center justify-center",
                ),
            ),
            class_name=rx.cond(
                show_warning_conv,
                "mt-4 relative border border-red-500 rounded-md p-2 inline-block",
                "mt-4 relative inline-block",
            ),
        ),
        class_name="bg-indigo-900 p-4 sm:p-6 rounded-lg shadow-lg h-full flex flex-col justify-between",
    )
