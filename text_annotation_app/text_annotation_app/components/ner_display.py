from typing import Tuple

import reflex as rx

from text_annotation_app.states.ner_state import (
    EntityInfo,
    NerState,
    Segment,
)


def entity_button(entity: EntityInfo) -> rx.Component:
    """Creates a button for an entity type with a remove option."""
    is_selected = NerState.selected_label_name == entity["name"]
    base_classes = f"px-3 py-1 {entity['color']} {entity['text_color']} rounded-md text-sm flex items-center transition-all duration-150 ease-in-out"
    selected_class_str = f"{base_classes} scale-105 shadow-md border-2 border-black"
    unselected_class_str = (
        f"{base_classes} hover:scale-105 shadow-sm border-2 border-transparent"
    )
    return rx.el.div(
        rx.el.span(
            entity["name"],
            class_name="font-semibold mr-2 cursor-pointer flex-grow",
            on_click=lambda: NerState.select_label(entity["name"]),
        ),
        rx.el.button(
            "X",
            on_click=lambda: NerState.remove_label(entity["name"]),
            class_name="ml-1 text-xs font-bold text-black/50 hover:text-black p-0.5 rounded-full w-4 h-4 flex items-center justify-center leading-none bg-white/40 hover:bg-white/70 transition-colors flex-shrink-0",
            title=f"Remove {entity['name']} label",
        ),
        class_name=rx.cond(
            is_selected,
            selected_class_str,
            unselected_class_str,
        ),
    )


def color_swatch(color_pair: rx.Var[Tuple[str, str]], index: int) -> rx.Component:
    """Creates a clickable color swatch.

    Args:
        color_pair: A Var representing the tuple (bg_color, text_color).
        index: The index of this color pair in the available_colors list.

    Returns:
        A component representing the color swatch.
    """
    bg_color = color_pair[0]
    is_selected = NerState.new_label_selected_color_index == index
    base_class = "w-6 h-6 rounded cursor-pointer transition-all duration-150 ease-in-out border-2"
    selected_class = f"{base_class} border-black scale-110"
    unselected_class = f"{base_class} border-transparent hover:scale-105"
    return rx.el.div(
        class_name=rx.cond(
            is_selected,
            f"{selected_class} {bg_color}",
            f"{unselected_class} {bg_color}",
        ),
        on_click=lambda: NerState.set_new_label_color_index(index),
        title=f"Select {bg_color}",
    )


def add_label_form() -> rx.Component:
    """Form to add new labels, including color selection."""
    return rx.el.div(
        rx.el.h3(
            "Add New Label",
            class_name="text-md font-semibold mb-3 text-gray-700",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Label Name (e.g., DATE)",
                on_change=NerState.set_new_label_name,
                class_name="border border-gray-300 rounded px-2 py-1 mr-2 flex-grow focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500",
                default_value=NerState.new_label_name,
            ),
            rx.el.input(
                placeholder="Keywords (comma-separated, optional)",
                on_change=NerState.set_new_label_keywords_str,
                class_name="border border-gray-300 rounded px-2 py-1 mr-2 flex-grow-[2] focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500",
                default_value=NerState.new_label_keywords_str,
            ),
            class_name="flex items-center gap-2 mb-3",
        ),
        rx.el.div(
            rx.el.label(
                "Select Color:",
                class_name="text-sm font-medium text-gray-600 mr-2 self-center",
            ),
            rx.el.div(
                rx.foreach(
                    NerState.available_colors,
                    lambda color, index: color_swatch(color, index),
                ),
                class_name="flex flex-wrap gap-2 items-center flex-grow",
            ),
            rx.el.button(
                "Add Label",
                on_click=NerState.add_new_label,
                class_name="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-1 rounded transition-colors shadow-sm ml-4 self-center",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="p-4 bg-gray-200 border-t border-gray-300",
    )


def header_bar() -> rx.Component:
    """Creates the header bar with entity buttons, add form, and download button."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Click a label below to select it, then click words in the text to apply/remove the label.",
                    class_name=rx.cond(
                        NerState.selected_label_name is None,
                        "text-sm text-gray-600 mb-2 px-4",
                        "hidden",
                    ),
                ),
                rx.el.p(
                    "Selected label: ",
                    rx.el.strong(NerState.selected_label_name),
                    " (Click words below to apply/remove)",
                    class_name=rx.cond(
                        NerState.selected_label_name is None,
                        "hidden",
                        "text-sm text-blue-700 font-semibold mb-2 px-4",
                    ),
                ),
                rx.el.div(
                    rx.foreach(NerState.entities, entity_button),
                    rx.el.button(
                        "Download Annotations",
                        on_click=rx.download(
                            data=NerState.annotated_text_json,
                            filename="annotated_text.json",
                        ),
                        class_name="bg-green-600 hover:bg-green-700 text-white font-semibold px-3 py-1 rounded text-sm transition-colors shadow-sm ml-auto",
                    ),
                    class_name="flex flex-wrap gap-2 p-4 items-center",
                ),
            )
        ),
        add_label_form(),
        class_name="bg-gray-100 border-b border-gray-300 rounded-t-lg shadow-sm sticky top-0 z-10",
    )


def render_segment(segment: Segment) -> rx.Component:
    """Renders a single text segment, making it clickable if a label is selected."""
    is_label_selected = NerState.selected_label_name is not None
    is_whitespace = segment["text"].strip() == ""
    base_component = rx.el.span(segment["text"])
    labeled_class = (
        segment["bg_color"]
        + " "
        + segment["text_color"]
        + " py-0.5 rounded-sm cursor-pointer"
    )
    labeled_component = rx.el.span(
        segment["text"],
        rx.el.span(
            segment["label_name"],
            class_name="text-[0.6rem] font-bold opacity-70 align-super",
        ),
        class_name=labeled_class,
        title=segment["label_name"],
    )
    hoverable_component = rx.el.span(
        segment["text"],
        class_name="hover:bg-gray-200 rounded-sm cursor-pointer transition-colors",
    )
    styled_component = rx.cond(
        segment["label_name"] is not None,
        labeled_component,
        rx.cond(
            is_label_selected & ~is_whitespace,
            hoverable_component,
            base_component,
        ),
    )
    on_click_event = rx.cond(
        is_label_selected & ~is_whitespace,
        NerState.apply_label(segment["id"]),
        rx.noop(),
    )
    clickable_component = rx.el.span(
        styled_component,
        on_click=on_click_event,
        class_name=rx.cond(segment["label_name"] is not None, "", "inline"),
    )
    return clickable_component


def text_display() -> rx.Component:
    """Displays the processed text with highlighted entities."""
    return rx.el.div(
        rx.el.p(
            rx.foreach(NerState.display_segments, render_segment),
            class_name="text-lg text-gray-800 whitespace-pre-wrap",
        ),
        class_name="p-6 bg-white border border-gray-300 border-t-0 rounded-b-lg shadow-inner",
    )


def ner_component() -> rx.Component:
    """The main component combining the header and text display."""
    return rx.el.div(
        header_bar(),
        text_display(),
        class_name="max-w-5xl mx-auto my-8 shadow-lg rounded-lg font-sans",
    )
