import reflex as rx

from weatherstack_app.components.preset_cards import preset_cards
from weatherstack_app.components.weather_display import weather_display
from weatherstack_app.states.weather_state import WeatherState


def index() -> rx.Component:
    return rx.el.div(
        rx.cond(
            WeatherState.display_weather,
            weather_display(),
            rx.el.div(
                rx.el.p(
                    "Where would you like the forecast for today?",
                    class_name="text-2xl md:text-3xl font-medium",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.div(
                            rx.el.button(
                                rx.icon(
                                    "forward",
                                    size=20,
                                    class_name="absolute right-2 top-1/2 transform -translate-y-1/2 rounded-full bg-blue-500 text-white p-2 disabled:opacity-50 shadow-sm size-7 self-flex items-center justify-center cursor-pointer",
                                ),
                                type="submit",
                            ),
                            rx.el.input(
                                name="city",
                                placeholder="Enter city name...",
                                default_value=WeatherState.city,
                                class_name="px-2 py-3 w-full text-sm rounded-xl bg-transparent border shadow-sm focus:outline-none focus:border-blue-500",
                            ),
                            class_name="relative focus:outline-none w-full max-w-[400px] py-4",
                        ),
                        class_name="flex w-full justify-center",
                    ),
                    on_submit=WeatherState.handle_form_submit,
                    reset_on_submit=False,
                    prevent_default=True,
                    class_name="w-full justify-center items-center flex",
                ),
                rx.cond(
                    WeatherState.error_message != "",
                    rx.el.p(
                        WeatherState.error_message,
                        class_name="text-sm font-medium text-red-500",
                    ),
                ),
                preset_cards(),
                class_name="flex flex-col items-center justify-center align-center min-h-screen gap-y-4",
            ),
        )
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)
