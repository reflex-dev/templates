import asyncio
import datetime
from typing import Dict, List, TypedDict

import reflex as rx

from futuristic_dashboard.states.data import (
    performance_chart_data,
    quick_actions_data,
    resource_allocation_data,
    stat_card_data,
    system_status_data,
)


class StatCardData(TypedDict):
    title: str
    value: str
    sub_detail: str
    icon: str
    color: str
    chart_data: List[Dict[str, int]]


class SystemStatusData(TypedDict):
    name: str
    value: int
    color: str


class ResourceAllocationData(TypedDict):
    name: str
    value: int
    color: str


class QuickActionData(TypedDict):
    name: str
    icon: str


class PerformanceChartData(TypedDict):
    time: str
    CPU: int
    Memory: int
    Network: int


class DashboardState(rx.State):
    """Holds the state for the dashboard."""

    current_time: str = datetime.datetime.now().strftime("%H:%M:%S")
    current_date: str = datetime.datetime.now().strftime("%b %d, %Y")
    uptime: str = "14d 06:42:18"
    time_zone: str = "UTC-08:00"
    active_nav: str = "Dashboard"
    active_performance_tab: str = "Performance"
    mobile_sidebar_open: bool = False
    stat_cards: List[StatCardData] = stat_card_data
    system_status: List[SystemStatusData] = system_status_data
    resource_allocation: List[ResourceAllocationData] = resource_allocation_data
    quick_actions: List[QuickActionData] = quick_actions_data
    performance_chart_data: List[PerformanceChartData] = performance_chart_data
    system_load: int = 35

    @rx.event(background=True)
    async def update_time(self):
        while True:
            async with self:
                self.current_time = datetime.datetime.now().strftime("%H:%M:%S")
                self.current_date = datetime.datetime.now().strftime("%b %d, %Y")
            await asyncio.sleep(1)

    @rx.event
    def set_active_nav(self, nav_item: str):
        self.active_nav = nav_item
        if self.mobile_sidebar_open:
            self.mobile_sidebar_open = False

    @rx.event
    def set_active_performance_tab(self, tab_name: str):
        self.active_performance_tab = tab_name

    @rx.event
    def toggle_mobile_sidebar(self):
        self.mobile_sidebar_open = not self.mobile_sidebar_open

    @rx.var
    def nav_items(self) -> List[Dict[str, str]]:
        return [
            {
                "name": "Dashboard",
                "icon": "layout-dashboard",
            },
            {"name": "Diagnostics", "icon": "activity"},
            {"name": "Data Center", "icon": "database"},
            {"name": "Network", "icon": "wifi"},
            {"name": "Security", "icon": "shield"},
            {"name": "Console", "icon": "terminal"},
            {
                "name": "Communications",
                "icon": "message-circle",
            },
            {"name": "Settings", "icon": "settings"},
        ]
