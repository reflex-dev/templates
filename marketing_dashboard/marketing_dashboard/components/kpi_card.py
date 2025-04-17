from typing import Union

import reflex as rx


def kpi_card(
    title: str,
    value: Union[str, int, rx.Var],
    description: str,
    class_name: str = "",
) -> rx.Component:
    """A card component to display a key performance indicator."""
    return rx.el.div(
        rx.el.p(
            title,
            class_name="text-sm font-medium text-gray-400 uppercase tracking-wider",
        ),
        rx.el.p(
            value,
            class_name="text-4xl sm:text-5xl font-bold text-white mt-2",
        ),
        rx.el.p(
            description,
            class_name="text-base text-gray-300 mt-1",
        ),
        class_name=f"bg-indigo-900 p-4 sm:p-6 rounded-lg shadow-lg {class_name}",
    )
