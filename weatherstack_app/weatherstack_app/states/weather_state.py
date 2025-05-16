from typing import List, TypedDict

import reflex as rx
import requests

WEATHERSTACK_API_KEY = "YOUR_WEATHERSTACK_API_KEY"
WEATHERSTACK_API_URL = "http://api.weatherstack.com/current"


class Location(TypedDict):
    name: str
    country: str
    region: str
    lat: str
    lon: str
    timezone_id: str
    localtime: str
    localtime_epoch: int
    utc_offset: str


class CurrentWeather(TypedDict):
    observation_time: str
    temperature: int
    weather_code: int
    weather_icons: List[str]
    weather_descriptions: List[str]
    wind_speed: int
    wind_degree: int
    wind_dir: str
    pressure: int
    precip: float
    humidity: int
    cloudcover: int
    feelslike: int
    uv_index: int
    visibility: int
    is_day: str


class WeatherRequest(TypedDict):
    type: str
    query: str
    language: str
    unit: str


class WeatherData(TypedDict):
    request: WeatherRequest | None
    location: Location | None
    current: CurrentWeather | None


class WeatherState(rx.State):
    city: str = ""
    weather_data: WeatherData | None = None
    loading: bool = False
    error_message: str = ""
    api_key: str = WEATHERSTACK_API_KEY

    @rx.event
    def reset_app(self):
        self.reset()
        return

    @rx.event
    def handle_form_submit(self, form_data: dict):
        self.city = form_data.get("city", "").strip()
        if not self.city:
            self.error_message = "City name cannot be empty."
            self.weather_data = None
            return
        self.error_message = ""
        return WeatherState.get_weather

    @rx.event
    def get_weather_from_preset(self, city: str):
        self.city = city
        if not self.city:
            self.error_message = "City name cannot be empty."
            self.weather_data = None
            return
        self.error_message = ""
        return WeatherState.get_weather

    @rx.event(background=True)
    async def get_weather(self):
        async with self:
            if not self.city:
                self.error_message = "City name cannot be empty."
                self.loading = False
                return
            if self.api_key == "YOUR_WEATHERSTACK_API_KEY":
                self.error_message = "Please replace 'YOUR_WEATHERSTACK_API_KEY' with your actual WeatherStack API key in app/states/weather_state.py."
                self.weather_data = None
                self.loading = False
                return
            self.loading = True
            self.error_message = ""
            self.weather_data = None
        try:
            params = {
                "access_key": self.api_key,
                "query": self.city,
            }
            response = requests.get(WEATHERSTACK_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            async with self:
                if "error" in data:
                    self.error_message = data["error"].get(
                        "info",
                        "An error occurred while fetching weather data.",
                    )
                    self.weather_data = None
                elif "current" in data and "location" in data:
                    self.weather_data = data
                    self.error_message = ""
                else:
                    self.error_message = "Unexpected API response format."
                    self.weather_data = None
        except requests.exceptions.RequestException as e:
            async with self:
                self.error_message = f"Network error: {e}"
                self.weather_data = None
        except Exception as e:
            async with self:
                self.error_message = f"An unexpected error occurred: {e}"
                self.weather_data = None
        finally:
            async with self:
                self.loading = False

    def set_city(self, city: str):
        self.city = city.strip()
        self.error_message = ""

    @rx.var
    def display_weather(self) -> bool:
        return (
            self.weather_data is not None
            and self.weather_data.get("current") is not None
            and (self.weather_data.get("location") is not None)
            and (not self.error_message)
        )

    @rx.var
    def weather_icon_url(self) -> str:
        if (
            self.display_weather
            and self.weather_data
            and self.weather_data.get("current")
            and self.weather_data["current"].get("weather_icons")
        ):
            return self.weather_data["current"]["weather_icons"][0]
        return ""

    @rx.var
    def weather_description_text(self) -> str:
        if (
            self.display_weather
            and self.weather_data
            and self.weather_data.get("current")
            and self.weather_data["current"].get("weather_descriptions")
        ):
            return ", ".join(self.weather_data["current"]["weather_descriptions"])
        return ""
