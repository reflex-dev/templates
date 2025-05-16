import reflex as rx

from weatherstack_app.states.weather_state import WeatherState


def card(flag: str, title: str, city: str) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.span(flag, class_name="text-xl"),
            rx.el.p(title, class_name="font-medium text-black text-base"),
            class_name="flex flex-row gap-2 items-center",
        ),
        type="button",
        class_name=(
            "flex flex-col gap-1 border bg-white hover:bg-gray-100 "
            "shadow-sm px-4 py-3.5 rounded-xl text-start transition-colors flex-1"
        ),
        on_click=WeatherState.get_weather_from_preset(city),
    )


def preset_cards() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            card("🇯🇵", "Tokyo, Japan", "Japan"),
            card("🇫🇷", "Paris, France", "France"),
            card("🇺🇸", "New York, USA", "USA"),
            card("🇦🇺", "Sydney, Australia", "Australia"),
            card("🇩🇪", "Berlin, Germany", "Germany"),
            card("🇧🇷", "São Paulo, Brazil", "Brazil"),
            card("🇨🇦", "Toronto, Canada", "Canada"),
            card("🇮🇳", "Mumbai, India", "India"),
            class_name="gap-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 w-full",
        ),
        class_name="flex flex-col justify-center items-center gap-8 w-full max-w-[55rem] px-6 md:pt-12",
    )
