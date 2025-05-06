import reflex as rx

from chat_app.components.typing_indicator import typing_indicator


def ai_bubble(message: str, is_last: bool = False) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("bot", size=16),
            class_name="rounded-full bg-white text-black p-2 size-8 inline-flex items-center justify-center border",
        ),
        rx.cond(
            message,
            rx.el.p(message, class_name="text-sm sm:text-base"),
            rx.cond(
                is_last,
                typing_indicator(),
            ),
        ),
        class_name="text-black text-base max-w-4xl flex flex-row gap-4",
    )


def user_bubble(message: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(message, class_name="text-sm sm:text-base"),
        class_name="text-white px-3 py-2 bg-blue-500 rounded-xl w-fit self-end max-w-[90%]",
    )


def message_bubble(
    message: str, is_ai: bool = False, is_last: bool = False
) -> rx.Component:
    return rx.el.div(
        rx.cond(
            is_ai,
            ai_bubble(message, is_last),
            user_bubble(message),
        ),
        class_name="w-full flex flex-col gap-6 mx-auto max-w-3xl px-8",
    )
