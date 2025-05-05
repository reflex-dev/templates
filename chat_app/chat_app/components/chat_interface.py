import reflex as rx

from chat_app.components.input_area import input_area
from chat_app.components.message_bubble import message_bubble
from chat_app.components.preset_cards import preset_cards
from chat_app.states.chat_state import ChatState


def chat_interface() -> rx.Component:
    """The main chat interface component."""
    return rx.el.div(
        rx.cond(
            ChatState.messages,
            rx.auto_scroll(
                rx.foreach(
                    ChatState.messages,
                    lambda m, i: message_bubble(
                        m["text"],
                        m["is_ai"],
                        i == ChatState.messages.length() - 1,
                    ),
                ),
                class_name="flex flex-col gap-4 pb-24 pt-6",
            ),
            preset_cards(),
        ),
        input_area(),
        class_name="h-screen flex flex-col bg-gray-50 w-full",
    )
