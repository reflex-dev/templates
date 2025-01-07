from typing import Dict, List

import reflex as rx
from reflex.components.radix.themes.base import (
    LiteralAccentColor,
)

from ..backend.backend import State


def _get_item_color(
    item: str, items_dict: Dict[str, LiteralAccentColor]
) -> rx.Component:
    return rx.match(item, *[(t, items_dict.get(t, "blue")) for t in items_dict], "blue")


badge_props = {
    "radius": "full",
    "variant": "surface",
    "size": "3",
    "margin": "5px",
    "cursor": "pointer",
    "style": {"_hover": {"opacity": 0.75}},
}


def _selected_item_badge(
    item_name: str, items_dict: Dict[str, LiteralAccentColor], item: str
) -> rx.Component:
    return rx.badge(
        item,
        rx.icon("x", size=18),
        color_scheme=_get_item_color(item, items_dict),
        **badge_props,
        on_click=lambda: State.remove_selected(item_name, item),
    )


def _unselected_item_badge(
    item_name: str, items_dict: Dict[str, LiteralAccentColor], items: List
) -> rx.Component:
    return rx.cond(
        State.selected_items[item_name].contains(items[0]),
        rx.box(),
        rx.badge(
            items[0],
            rx.icon("plus", size=18),
            color_scheme=_get_item_color(items[0], items_dict),
            **badge_props,
            on_click=lambda: State.add_selected(item_name, items[0]),
        ),
    )


def _badge(text: str, color_scheme: LiteralAccentColor) -> rx.Component:
    return rx.badge(
        text, color_scheme=color_scheme, radius="large", variant="surface", size="3"
    )


def item_badge(item: str, item_dict: Dict[str, LiteralAccentColor]) -> rx.Component:
    return rx.match(
        item,
        *[(t, _badge(t, item_dict.get(t, "blue"))) for t in item_dict],
        _badge("item", "blue"),
    )
