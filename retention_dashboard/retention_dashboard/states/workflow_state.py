from typing import Dict, List, TypedDict

import reflex as rx


class ChartData(TypedDict):
    name: str
    value: int
    percentage: float
    fill: str


class WorkflowState(rx.State):
    """State for the Workflow tab."""

    test_quota: int = 34
    departments: List[str] = [
        "Customer Service",
        "Technical Support",
        "Billing Support",
        "Claims Processing",
        "Account Management",
        "Sales Support",
    ]
    excluded_departments: Dict[str, bool] = {dept: False for dept in departments}
    completed_cases_data: list[ChartData] = [
        {
            "name": "Completed",
            "value": 11327,
            "percentage": 100.0,
            "fill": "#3b82f6",
        }
    ]
    test_results_data_tested: list[ChartData] = [
        {
            "name": "Tested",
            "value": 3874,
            "percentage": 34.2,
            "fill": "#3b82f6",
        }
    ]
    test_results_data_untested: list[ChartData] = [
        {
            "name": "Untested",
            "value": 7453,
            "percentage": 65.8,
            "fill": "#d1d5db",
        }
    ]
    impact_data_error_free: list[ChartData] = [
        {
            "name": "Error-free",
            "value": 3413,
            "percentage": 30.1,
            "fill": "#10b981",
        }
    ]
    impact_data_corrected: list[ChartData] = [
        {
            "name": "Corrected",
            "value": 461,
            "percentage": 4.1,
            "fill": "#ef4444",
        }
    ]

    @rx.event
    def set_test_quota(self, value: str):
        """Sets the test quota value from the slider."""
        self.test_quota = int(value)

    @rx.event
    def toggle_department(self, dept_name: str):
        """Toggles the exclusion status of a department."""
        self.excluded_departments[dept_name] = not self.excluded_departments[dept_name]
