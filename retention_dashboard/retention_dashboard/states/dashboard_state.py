from typing import Literal

import reflex as rx


class DashboardState(rx.State):
    """State to manage the active tab in the dashboard."""

    active_tab: Literal["Support", "Retention", "Workflow", "Agents"] = "Retention"

    @rx.event
    def set_active_tab(
        self,
        tab: Literal["Support", "Retention", "Workflow", "Agents"],
    ):
        """Sets the active tab."""
        self.active_tab = tab
