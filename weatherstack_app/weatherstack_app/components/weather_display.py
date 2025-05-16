import reflex as rx
from weatherstack_app.states.weather_state import WeatherState


def weather_display() -> rx.Component:
    return rx.el.div(
        rx.cond(
            WeatherState.loading,
            rx.el.div(
                rx.spinner(class_name="text-blue-500"),
                rx.el.p(
                    "Loading weather data...",
                    class_name="text-lg text-gray-600",
                ),
                class_name="flex flex-col items-center justify-center p-6 bg-white rounded-lg shadow-md",
            ),
            rx.cond(
                WeatherState.error_message != "",
                rx.el.div(
                    rx.el.p(
                        "Error:",
                        class_name="font-semibold text-red-600",
                    ),
                    rx.el.p(
                        WeatherState.error_message,
                        class_name="text-red-500",
                    ),
                    class_name="p-6 bg-red-50 rounded-lg shadow-md border border-red-200",
                ),
                rx.cond(
                    WeatherState.display_weather,
                    rx.el.div(
                        rx.el.p(
                            f"{WeatherState.weather_data['location']['name']}, {WeatherState.weather_data['location']['country']}",
                            class_name="text-3xl font-bold text-gray-800 mb-4",
                        ),
                        rx.el.div(
                            rx.el.img(
                                src=WeatherState.weather_icon_url,
                                alt="Weather icon",
                                class_name="w-20 h-20 mb-2",
                            ),
                            rx.el.p(
                                WeatherState.weather_description_text,
                                class_name="text-xl text-gray-700 capitalize",
                            ),
                            class_name="flex flex-col items-center mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Temperature:",
                                    class_name="text-md text-gray-600",
                                ),
                                rx.el.p(
                                    f"{WeatherState.weather_data['current']['temperature']}°C",
                                    class_name="text-2xl font-semibold text-blue-600",
                                ),
                                class_name="p-4 bg-blue-50 rounded-lg shadow-sm text-center",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Humidity:",
                                    class_name="text-md text-gray-600",
                                ),
                                rx.el.p(
                                    f"{WeatherState.weather_data['current']['humidity']}%",
                                    class_name="text-2xl font-semibold text-green-600",
                                ),
                                class_name="p-4 bg-green-50 rounded-lg shadow-sm text-center",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Feels Like:",
                                    class_name="text-md text-gray-600",
                                ),
                                rx.el.p(
                                    f"{WeatherState.weather_data['current']['feelslike']}°C",
                                    class_name="text-2xl font-semibold text-orange-600",
                                ),
                                class_name="p-4 bg-orange-50 rounded-lg shadow-sm text-center",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Wind Speed:",
                                    class_name="text-md text-gray-600",
                                ),
                                rx.el.p(
                                    f"{WeatherState.weather_data['current']['wind_speed']} km/h",
                                    class_name="text-2xl font-semibold text-purple-600",
                                ),
                                class_name="p-4 bg-purple-50 rounded-lg shadow-sm text-center",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 w-full",
                        ),
                        rx.button("Reset", on_click=WeatherState.reset_app),
                        class_name="p-6 rounded-lg border shadow-sm border w-full max-w-2xl justify-center",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Enter a city to get the weather forecast.",
                            class_name="text-lg text-gray-500",
                        ),
                        class_name="p-6 bg-white rounded-lg shadow-md",
                    ),
                ),
            ),
        ),
        class_name="mt-8 w-full flex justify-center",
    )
