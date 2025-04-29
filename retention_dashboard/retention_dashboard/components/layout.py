import reflex as rx

from retention_dashboard.components.retention import retention_component
from retention_dashboard.components.workflow import workflow_component
from retention_dashboard.states.dashboard_state import DashboardState


def nav_button(text: str, is_active: rx.Var[bool]) -> rx.Component:
    """Creates a navigation button."""
    return rx.el.button(
        text,
        on_click=lambda: DashboardState.set_active_tab(text),
        class_name=rx.cond(
            is_active,
            "px-4 py-2 text-sm font-medium text-blue-700 bg-blue-100 rounded-md",
            "px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-md",
        ),
    )


def placeholder_component(title: str) -> rx.Component:
    """A placeholder component for inactive tabs."""
    return rx.el.div(
        rx.el.h2(
            title,
            class_name="text-2xl font-semibold text-gray-800 mb-2",
        ),
        rx.el.p(
            f"Content for {title} goes here.",
            class_name="text-gray-600",
        ),
        class_name="p-6 bg-white rounded-lg shadow h-96 flex items-center justify-center",
    )


def layout() -> rx.Component:
    """The main layout for the dashboard."""
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.h1(
                    "Overview",
                    class_name="text-xl font-semibold text-gray-800",
                ),
                rx.el.div(
                    rx.icon(
                        tag="bell",
                        class_name="text-gray-500 hover:text-gray-700 cursor-pointer",
                    ),
                    rx.el.button(
                        "ES",
                        class_name="ml-4 px-3 py-1 text-xs font-medium text-gray-600 border rounded hover:bg-gray-100",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center justify-between px-6 py-4 border-b border-gray-200",
            )
        ),
        rx.el.main(
            rx.el.nav(
                nav_button(
                    "Support",
                    DashboardState.active_tab == "Support",
                ),
                nav_button(
                    "Retention",
                    DashboardState.active_tab == "Retention",
                ),
                nav_button(
                    "Workflow",
                    DashboardState.active_tab == "Workflow",
                ),
                nav_button(
                    "Agents",
                    DashboardState.active_tab == "Agents",
                ),
                class_name="flex space-x-4 px-6 py-3 border-b border-gray-200 overflow-x-auto w-[90%]",
            ),
            rx.el.div(
                rx.match(
                    DashboardState.active_tab,
                    ("Retention", retention_component()),
                    ("Workflow", workflow_component()),
                    (
                        "Support",
                        placeholder_component("Support"),
                    ),
                    (
                        "Agents",
                        placeholder_component("Agents"),
                    ),
                    placeholder_component("Unknown"),
                ),
                class_name="p-6",
            ),
            class_name="flex-grow",
        ),
        class_name="min-h-screen flex flex-col bg-gray-50",
    )
