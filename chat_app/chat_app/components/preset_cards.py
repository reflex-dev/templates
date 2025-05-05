import reflex as rx

from chat_app.states.chat_state import ChatState


def card(icon: str, title: str, description: str, color: str) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.icon(tag=icon, size=16, class_name=f"stroke-{color}-500"),
            rx.el.p(title, class_name="font-medium text-black text-base"),
            class_name="flex flex-row gap-2 items-center",
        ),
        rx.el.p(description, class_name="text-gray-500 text-sm font-medium"),
        on_click=ChatState.send_message({"message": description}),
        type="button",
        class_name="flex flex-col gap-1 border bg-white hover:bg-gray-100 shadow-sm px-4 py-3.5 rounded-xl text-start transition-colors flex-1",
    )


def preset_cards() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("bot", size=24),
                class_name="rounded-full bg-whit p-2 size-10 inline-flex items-center justify-center border",
            ),
            rx.el.p(
                "How can I help you today?",
                class_name="text-2xl md:text-3xl font-medium",
            ),
            class_name="text-black flex flex-row gap-4 items-center",
        ),
        rx.el.div(
            card(
                "message-circle",
                "Ask a question",
                "What is the capital of France?",
                "green",
            ),
            card(
                "calculator",
                "Solve a math problem",
                "What is the square root of 144?",
                "rose",
            ),
            card(
                "globe",
                "Get a fun fact",
                "Tell me an interesting fact about dolphins.",
                "blue",
            ),
            card(
                "book",
                "Recommend a book",
                "What's a good mystery novel for beginners?",
                "amber",
            ),
            class_name="gap-4 grid grid-cols-1 lg:grid-cols-2 w-full",
        ),
        class_name="top-1/3 left-1/2 absolute flex flex-col justify-center items-center gap-8 w-full max-w-[44rem] transform -translate-x-1/2 -translate-y-1/2 px-6",
    )
