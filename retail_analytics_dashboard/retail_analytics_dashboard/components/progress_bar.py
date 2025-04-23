import reflex as rx

from retail_analytics_dashboard.states.dashboard_state import DashboardState


def progress_bar(
    label: rx.Var[str],
    value: rx.Var[str],
    total: rx.Var[str],
    percentage: rx.Var[float],
) -> rx.Component:
    """A simple progress bar component."""
    return rx.el.div(
        rx.el.div(
            rx.el.p(label, class_name="text-sm text-gray-600"),
            rx.el.p(
                f"{value} / {total}",
                class_name="text-sm font-medium text-gray-800",
            ),
            class_name="flex justify-between mb-1",
        ),
        rx.el.div(
            rx.el.div(
                class_name="bg-indigo-600 h-2 rounded-full",
                style={"width": percentage.to_string() + "%"},
            ),
            class_name="w-full bg-gray-200 rounded-full h-2",
        ),
    )


def cost_progress_bar(
    items: rx.Var[list[dict]],
) -> rx.Component:
    """A multi-segment progress bar for costs with remaining budget display."""
    return rx.el.div(
        rx.el.div(
            rx.foreach(
                items,
                lambda item: rx.el.div(
                    class_name=item["color"]
                    + " h-2 first:rounded-l-full last:rounded-r-full",
                    style={"width": item["percentage"].to_string() + "%"},
                ),
            ),
            class_name="flex w-full bg-gray-200 rounded-full h-2 overflow-hidden",
        ),
        rx.el.div(
            rx.foreach(
                items,
                lambda item: rx.el.div(
                    rx.el.span(class_name="w-2 h-2 rounded-full mr-2 " + item["color"]),
                    rx.el.span(
                        f"{item['label']} ({item['value']} / {item['percentage']}%)",
                        class_name="text-xs text-gray-600",
                    ),
                    class_name="flex items-center",
                ),
            ),
            class_name="mt-2 space-y-1",
        ),
        rx.el.p(
            "Remaining $",
            DashboardState.remaining_budget_value.to_string(),
            " (",
            DashboardState.remaining_budget_percentage.to_string(),
            "%) / $",
            DashboardState.total_budget.to_string(),
            class_name="text-xs text-gray-500 mt-2 text-right",
        ),
    )
