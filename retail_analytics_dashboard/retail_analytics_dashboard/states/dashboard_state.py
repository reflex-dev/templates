import reflex as rx
from typing import TypedDict, List, Union, Dict, Any
import random
import datetime

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "borderColor": "#E8E8E8",
        "borderRadius": "0.75rem",
        "boxShadow": "0px 24px 12px 0px light-dark(rgba(28, 32, 36, 0.02), rgba(0, 0, 0, 0.00)), 0px 8px 8px 0px light-dark(rgba(28, 32, 36, 0.02), rgba(0, 0, 0, 0.00)), 0px 2px 6px 0px light-dark(rgba(28, 32, 36, 0.02), rgba(0, 0, 0, 0.00))",
        "fontFamily": "sans-serif",
        "fontSize": "0.875rem",
        "lineHeight": "1.25rem",
        "fontWeight": "500",
        "minWidth": "8rem",
        "padding": "0.375rem 0.625rem",
        "position": "relative",
    },
    "item_style": {
        "display": "flex",
        "paddingBottom": "0px",
        "position": "relative",
        "paddingTop": "2px",
    },
    "label_style": {
        "color": "black",
        "fontWeight": "500",
        "alignSelf": "flex-end",
    },
    "separator": "",
}


class NavItem(TypedDict):
    name: str
    icon: str
    active: bool


class ShortcutItem(TypedDict):
    name: str
    icon: str


class BillingStat(TypedDict):
    label: str
    value: str
    total: str
    percentage: float


class CostItem(TypedDict):
    label: str
    value: str
    value_num: float
    percentage: float
    color: str


class ChartDataPoint(TypedDict):
    date: str
    value1: int
    value2: int


class OverviewMetric(TypedDict):
    id: str
    title: str
    change: str
    change_color: str
    value: str
    previous_value: str
    chart_data: List[ChartDataPoint]


def generate_chart_data(
    start_date_str: str,
    end_date_str: str,
    num_points: int = 30,
    min_val1: int = 50,
    max_val1: int = 200,
    min_val2: int = 30,
    max_val2: int = 150,
) -> List[ChartDataPoint]:
    data: List[ChartDataPoint] = []
    start_date = datetime.datetime.strptime(
        start_date_str, "%d/%m/%Y"
    )
    end_date = datetime.datetime.strptime(
        end_date_str, "%d/%m/%Y"
    )
    date_delta = (end_date - start_date) / (num_points - 1)
    for i in range(num_points):
        current_date = start_date + date_delta * i
        data.append(
            {
                "date": current_date.strftime("%d/%m/%Y"),
                "value1": random.randint(
                    min_val1, max_val1
                ),
                "value2": random.randint(
                    min_val2, max_val2
                ),
            }
        )
    return data


overview_metrics_data: List[OverviewMetric] = [
    {
        "id": "rows_read",
        "title": "Rows read",
        "change": "+4.4%",
        "change_color": "text-green-600",
        "value": "643,015",
        "previous_value": "from 615,752",
        "chart_data": generate_chart_data(
            "16/04/2024",
            "16/05/2024",
            min_val1=600000,
            max_val1=650000,
            min_val2=610000,
            max_val2=630000,
        ),
    },
    {
        "id": "rows_written",
        "title": "Rows written",
        "change": "-3.9%",
        "change_color": "text-red-600",
        "value": "83,197",
        "previous_value": "from 86,580",
        "chart_data": generate_chart_data(
            "16/04/2024",
            "16/05/2024",
            min_val1=80000,
            max_val1=90000,
            min_val2=82000,
            max_val2=88000,
        ),
    },
    {
        "id": "queries",
        "title": "Queries",
        "change": "-0.9%",
        "change_color": "text-red-600",
        "value": "14,447",
        "previous_value": "from 14,573",
        "chart_data": generate_chart_data(
            "16/04/2024",
            "16/05/2024",
            min_val1=14000,
            max_val1=15000,
            min_val2=14200,
            max_val2=14800,
        ),
    },
    {
        "id": "costs",
        "title": "Costs",
        "change": "-1.4%",
        "change_color": "text-red-600",
        "value": "$293.5",
        "previous_value": "from $297.7",
        "chart_data": generate_chart_data(
            "16/04/2024",
            "16/05/2024",
            min_val1=280,
            max_val1=310,
            min_val2=290,
            max_val2=300,
        ),
    },
    {
        "id": "payments_completed",
        "title": "Payments completed",
        "change": "-9.6%",
        "change_color": "text-red-600",
        "value": "$2,850.00",
        "previous_value": "from $3,153.00",
        "chart_data": generate_chart_data(
            "16/04/2024",
            "16/05/2024",
            min_val1=2800,
            max_val1=3200,
            min_val2=2900,
            max_val2=3100,
        ),
    },
    {
        "id": "sign_ups",
        "title": "Sign ups",
        "change": "+7.2%",
        "change_color": "text-green-600",
        "value": "2,098",
        "previous_value": "from 1,957",
        "chart_data": generate_chart_data(
            "16/04/2024",
            "16/05/2024",
            min_val1=1900,
            max_val1=2200,
            min_val2=1950,
            max_val2=2150,
        ),
    },
    {
        "id": "logins",
        "title": "Logins",
        "change": "-9.0%",
        "change_color": "text-red-600",
        "value": "43,243",
        "previous_value": "from 47,538",
        "chart_data": generate_chart_data(
            "16/04/2024",
            "16/05/2024",
            min_val1=42000,
            max_val1=49000,
            min_val2=43000,
            max_val2=48000,
        ),
    },
    {
        "id": "support_calls",
        "title": "Support calls",
        "change": "+67.1%",
        "change_color": "text-green-600",
        "value": "127",
        "previous_value": "from 76",
        "chart_data": generate_chart_data(
            "16/04/2024",
            "16/05/2024",
            min_val1=70,
            max_val1=140,
            min_val2=80,
            max_val2=130,
        ),
    },
]


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
    overview_metrics: List[OverviewMetric] = (
        overview_metrics_data
    )
    chart_visibility: Dict[str, bool] = {
        metric["id"]: True
        for metric in overview_metrics_data
    }
    temp_chart_visibility: Dict[str, bool] = {}
    show_customize_dialog: bool = False

    @rx.var
    def current_total_cost(self) -> float:
        """Calculates the current total cost from the breakdown items."""
        return sum(
            (
                item["value_num"]
                for item in self.billing_costs_items
            )
        )

    @rx.var
    def remaining_budget_value(self) -> float:
        """Calculates the remaining budget value."""
        return self.total_budget - self.current_total_cost

    @rx.var
    def remaining_budget_percentage(self) -> float:
        """Calculates the remaining budget percentage."""
        if self.total_budget == 0:
            return 0.0
        percentage = (
            self.remaining_budget_value
            / self.total_budget
            * 100
        )
        return round(percentage * 10) / 10

    @rx.var
    def total_cost_percentage(self) -> float:
        """Calculates the total percentage used based on cost items."""
        return sum(
            (
                item["percentage"]
                for item in self.billing_costs_items
            )
        )

    @rx.var
    def visible_overview_metrics(
        self,
    ) -> List[OverviewMetric]:
        """Returns the list of overview metrics that are marked as visible."""
        return [
            metric
            for metric in self.overview_metrics
            if self.chart_visibility.get(
                metric["id"], False
            )
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
        self.show_customize_dialog = (
            not self.show_customize_dialog
        )
        if self.show_customize_dialog:
            self.temp_chart_visibility = (
                self.chart_visibility.copy()
            )

    @rx.event
    def toggle_temp_chart_visibility(self, chart_id: str):
        """Toggles the visibility of a specific chart in the temporary state."""
        if chart_id in self.temp_chart_visibility:
            self.temp_chart_visibility[chart_id] = (
                not self.temp_chart_visibility[chart_id]
            )

    @rx.event
    def apply_chart_visibility(self):
        """Applies the temporary visibility settings to the actual state and closes the dialog."""
        self.chart_visibility = (
            self.temp_chart_visibility.copy()
        )
        self.show_customize_dialog = False

    @rx.event
    def cancel_chart_visibility(self):
        """Closes the dialog without applying changes."""
        self.show_customize_dialog = False