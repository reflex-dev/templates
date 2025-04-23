from typing import List, Optional, TypedDict

import reflex as rx

from retention_dashboard.states.data import retention_data_raw


class RetentionWeekData(TypedDict):
    value: Optional[float]
    count: Optional[int]


class RetentionCohortData(TypedDict):
    cohort: str
    initial_customers: int
    weeks: List[RetentionWeekData]


class RetentionState(rx.State):
    """State for the Cohort Retention tab."""

    column_headers: list[str] = [
        "Cohort",
        "Week 0",
        "Week 1",
        "Week 2",
        "Week 3",
        "Week 4",
        "Week 5",
        "Week 6",
        "Week 7",
        "Week 8",
        "Week 9",
    ]
    retention_data: list[RetentionCohortData] = retention_data_raw

    def get_cell_color(self, percentage: float) -> str:
        """Returns background color based on percentage."""
        if percentage >= 80:
            return "bg-blue-600"
        elif percentage >= 60:
            return "bg-blue-500"
        elif percentage >= 40:
            return "bg-blue-400"
        elif percentage >= 20:
            return "bg-blue-300"
        elif percentage > 0:
            return "bg-blue-200"
        return "bg-gray-100"
