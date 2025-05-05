import reflex as rx

from chat_app.states.chat_state import ChatState


def input_area() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.form(
                rx.el.textarea(
                    name="message",
                    placeholder="Ask me anything",
                    enter_key_submit=True,
                    class_name="bg-transparent resize-none outline-none text-base py-2 px-3 min-h-10 text-black max-h-36 peer !overflow-y-auto",
                    auto_height=True,
                    required=True,
                ),
                rx.box(
                    rx.cond(
                        ChatState.messages,
                        rx.el.button(
                            rx.icon("square-pen", size=16),
                            title="New chat",
                            class_name="rounded-full bg-white text-gray-500 p-2 shadow-sm size-9 inline-flex items-center justify-center hover:bg-gray-100 border transition-colors",
                            type="button",
                            on_click=ChatState.clear_messages,
                        ),
                    ),
                    rx.el.button(
                        rx.cond(
                            ChatState.typing,
                            rx.icon("loader-circle", class_name="animate-spin"),
                            rx.icon("arrow-up"),
                        ),
                        class_name="self-end rounded-full bg-blue-500 text-white p-2 disabled:opacity-50 shadow-sm size-9 inline-flex items-center justify-center",
                        disabled=ChatState.typing,
                    ),
                    class_name="flex flex-row mb-2 peer-placeholder-shown:[&>*:last-child]:opacity-50 peer-placeholder-shown:[&>*:last-child]:pointer-events-none w-full",
                    justify_content=rx.cond(
                        ChatState.messages,
                        "space-between",
                        "end",
                    ),
                ),
                reset_on_submit=True,
                on_submit=ChatState.send_message,
                class_name="flex flex-col gap-2",
            ),
            class_name="rounded-3xl bg-background w-full border px-3 py-1 shadow-sm mx-auto z-10 focus-within:ring-blue-100 focus-within:ring-2 focus-within:shadow-none bg-white",
        ),
        class_name="px-6 fixed bottom-6 left-0 right-0 max-w-3xl mx-auto",
    )
