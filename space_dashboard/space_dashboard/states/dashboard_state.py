from typing import List, TypedDict

import reflex as rx


class EnvData(TypedDict):
    label: str
    value: str
    unit: str
    icon: str


class PlanetData(TypedDict):
    name: str
    distance: str
    color: str


class ComData(TypedDict):
    channel: str
    value: int


class PosData(TypedDict):
    label: str
    value: int


class StreamData(TypedDict):
    label: str
    value: int


class DashboardState(rx.State):
    """Holds the state for the Ares Dashboard."""

    environment_data: List[EnvData] = [
        {
            "label": "PRESSURE",
            "value": "15.65",
            "unit": "PSI",
            "icon": "gauge",
        },
        {
            "label": "OXYGEN",
            "value": "29.15",
            "unit": "%",
            "icon": "wind",
        },
        {
            "label": "TEMPERATURE",
            "value": "5.3",
            "unit": "C°",
            "icon": "thermometer",
        },
    ]
    planets_data: List[PlanetData] = [
        {
            "name": "MARS",
            "distance": "1.67 L.Y.",
            "color": "bg-orange-600",
        },
        {
            "name": "EARTH",
            "distance": "1.62 L.Y.",
            "color": "bg-blue-600",
        },
        {
            "name": "SATURN",
            "distance": "2.22 L.Y.",
            "color": "bg-yellow-400",
        },
    ]
    current_speed: int = 16540
    control_buttons: List[str] = [
        "DATA_DRIVE",
        "PO_DATABASE",
        "ACTIVE_ROUTE",
        "AUTO_PILOT",
    ]
    hq_coms_data: List[ComData] = [
        {"channel": "C1", "value": 40},
        {"channel": "C2", "value": 60},
        {"channel": "C3", "value": 80},
        {"channel": "C4", "value": 90},
        {"channel": "C5", "value": 20},
        {"channel": "C6", "value": 30},
    ]
    pos_tracking_data: List[PosData] = [
        {"label": "X", "value": 95},
        {"label": "Y", "value": 49},
        {"label": "Z", "value": 59},
        {"label": "V", "value": 60},
    ]
    data_stream_data: List[StreamData] = [
        {"label": "AT1", "value": 148},
        {"label": "SR1", "value": 30},
        {"label": "AF1", "value": 123},
        {"label": "AT2", "value": 180},
        {"label": "SR2", "value": 680},
        {"label": "AF2", "value": 15},
    ]
    alert_value: int = 798
    user_status: str = "USER_LOGGED_IN"
    live_status: str = "[LIVE]"
