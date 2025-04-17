import reflex as rx
from typing import List, Dict, Union


def data_list_card(
    title: str,
    data: rx.Var[List[Dict[str, Union[str, int]]]],
    value_key: str = "value",
) -> rx.Component:
    """A card component to display data in a simple list format."""
    return rx.el.div(
        rx.el.p(
            title,
            class_name="text-sm font-medium text-gray-400 uppercase tracking-wider mb-4",
        ),
        rx.el.div(
            rx.foreach(
                data,
                lambda item: rx.el.div(
                    rx.el.span(
                        item["medium"],
                        class_name="text-gray-300",
                    ),
                    rx.el.span(
                        item[value_key],
                        class_name="text-white font-medium",
                    ),
                    class_name="flex justify-between items-center py-2 border-b border-gray-700 last:border-b-0",
                ),
            ),
            class_name="space-y-1 text-sm",
        ),
        class_name="bg-indigo-900 p-4 sm:p-6 rounded-lg shadow-lg h-full",
    )
