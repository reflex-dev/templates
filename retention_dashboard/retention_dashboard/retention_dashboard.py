import reflex as rx
from retention_dashboard.components.layout import layout
from retention_dashboard.states.dashboard_state import DashboardState
from retention_dashboard.states.retention_state import RetentionState
from retention_dashboard.states.workflow_state import WorkflowState


def index() -> rx.Component:
    """The main page of the app."""
    return layout()


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index, route="/")