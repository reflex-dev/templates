from typing import Dict, List

import reflex as rx

from retail_analytics_dashboard.models.models import (
    BillingStat,
    CostItem,
    NavItem,
    OverviewMetric,
    ShortcutItem,
)
from retail_analytics_dashboard.states.data import overview_metrics_data


class DashboardState(rx.State):
    nav_items: List[NavItem] = [
        {
            "name": "Overview",
            "icon": "home",
            "active": True,
        },
        {
            "name": "Details",
            "icon": "list",
            "active": False,
        },
        {
            "name": "Settings",
            "icon": "settings",
            "active": False,
        },
    ]
    shortcuts: List[ShortcutItem] = [
        {"name": "Add new user", "icon": "link"},
        {"name": "Workspace usage", "icon": "link"},
        {"name": "Cost spend control", "icon": "link"},
        {"name": "Overview - Rows written", "icon": "link"},
    ]
    billing_usage_stats: List[BillingStat] = [
        {
            "label": "Rows read",
            "value": "48.1M",
            "total": "100M",
            "percentage": 48.1,
        },
        {
            "label": "Rows written",
            "value": "78.3M",
            "total": "100M",
            "percentage": 78.3,
        },
        {
            "label": "Storage",
            "value": "5.2GB",
            "total": "20GB",
            "percentage": 26.0,
        },
    ]
    billing_workspace_stats: List[BillingStat] = [
        {
            "label": "Weekly active users",
            "value": "21.7%",
            "total": "100%",
            "percentage": 21.7,
        },
        {
            "label": "Total users",
            "value": "28",
            "total": "40",
            "percentage": 70.0,
        },
        {
            "label": "Uptime",
            "value": "98.3%",
            "total": "100%",
            "percentage": 98.3,
        },
    ]
    total_budget: float = 328.0
    billing_costs_items: List[CostItem] = [
        {
            "label": "Base tier",
            "value": "$200",
            "value_num": 200.0,
            "percentage": 68.1,
            "color": "bg-indigo-600",
        },
        {
            "label": "On-demand charges",
            "value": "$61.1",
            "value_num": 61.1,
            "percentage": 20.8,
            "color": "bg-purple-600",
        },
        {
            "label": "Caching",
            "value": "$31.9",
            "value_num": 31.9,
            "percentage": 11.1,
            "color": "bg-gray-400",
        },
    ]
    overview_metrics: List[OverviewMetric] = overview_metrics_data
    chart_visibility: Dict[str, bool] = {
        metric["id"]: True for metric in overview_metrics_data
    }
    temp_chart_visibility: Dict[str, bool] = {}
    show_customize_dialog: bool = False

    @rx.var
    def current_total_cost(self) -> float:
        """Calculates the current total cost from the breakdown items."""
        return sum((item["value_num"] for item in self.billing_costs_items))

    @rx.var
    def remaining_budget_value(self) -> float:
        """Calculates the remaining budget value."""
        return self.total_budget - self.current_total_cost

    @rx.var
    def remaining_budget_percentage(self) -> float:
        """Calculates the remaining budget percentage."""
        if self.total_budget == 0:
            return 0.0
        percentage = self.remaining_budget_value / self.total_budget * 100
        return round(percentage * 10) / 10

    @rx.var
    def total_cost_percentage(self) -> float:
        """Calculates the total percentage used based on cost items."""
        return sum((item["percentage"] for item in self.billing_costs_items))

    @rx.var
    def visible_overview_metrics(
        self,
    ) -> List[OverviewMetric]:
        """Returns the list of overview metrics that are marked as visible."""
        return [
            metric
            for metric in self.overview_metrics
            if self.chart_visibility.get(metric["id"], False)
        ]

    @rx.event
    def set_active_nav(self, item_name: str):
        new_nav_items = []
        for item in self.nav_items:
            new_item = item.copy()
            new_item["active"] = item["name"] == item_name
            new_nav_items.append(new_item)
        self.nav_items = new_nav_items

    @rx.event
    def toggle_customize_dialog(self):
        """Toggles the customize charts dialog and initializes temporary visibility."""
        self.show_customize_dialog = not self.show_customize_dialog
        if self.show_customize_dialog:
            self.temp_chart_visibility = self.chart_visibility.copy()

    @rx.event
    def toggle_temp_chart_visibility(self, chart_id: str):
        """Toggles the visibility of a specific chart in the temporary state."""
        if chart_id in self.temp_chart_visibility:
            self.temp_chart_visibility[chart_id] = not self.temp_chart_visibility[
                chart_id
            ]

    @rx.event
    def apply_chart_visibility(self):
        """Applies the temporary visibility settings to the actual state and closes the dialog."""
        self.chart_visibility = self.temp_chart_visibility.copy()
        self.show_customize_dialog = False

    @rx.event
    def cancel_chart_visibility(self):
        """Closes the dialog without applying changes."""
        self.show_customize_dialog = False
