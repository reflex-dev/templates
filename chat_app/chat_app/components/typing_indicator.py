import reflex as rx


def typing_indicator() -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name="size-1.5 bg-gray-500 rounded-full animate-bounce"),
        rx.el.div(
            class_name="size-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]"
        ),
        rx.el.div(
            class_name="size-1.5 bg-gray-500 rounded-full animate-bounce [animation-delay:0.4s]"
        ),
        class_name="flex gap-1 justify-center items-center",
    )
