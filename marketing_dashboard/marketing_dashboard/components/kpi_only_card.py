from typing import Union

import reflex as rx


def kpi_only_card(
    primary_value: Union[int, str, rx.Var],
    primary_desc: str,
    secondary_value: Union[str, rx.Var],
    secondary_desc: str,
    show_warning: bool = False,
) -> rx.Component:
    """A card specifically for the bottom right two KPIs."""
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                primary_value,
                class_name="text-4xl sm:text-5xl font-bold text-white",
            ),
            rx.el.p(
                primary_desc,
                class_name="text-sm text-gray-300 mt-1",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    secondary_value,
                    class_name="text-4xl sm:text-5xl font-bold text-white",
                ),
                rx.el.p(
                    secondary_desc,
                    class_name="text-sm text-gray-300 mt-1",
                ),
                rx.cond(
                    show_warning,
                    rx.el.div(
                        rx.el.span(
                            "!",
                            class_name="text-white font-bold text-xs",
                        ),
                        class_name="absolute -top-2 -right-2 bg-red-500 rounded-full w-5 h-5 flex items-center justify-center",
                    ),
                ),
                class_name=rx.cond(
                    show_warning,
                    "relative border border-red-500 rounded-md p-3 inline-block",
                    "relative inline-block",
                ),
            )
        ),
        class_name="bg-indigo-900 p-4 sm:p-6 rounded-lg shadow-lg h-full flex flex-col justify-center",
    )
