import reflex as rx

from retention_dashboard.states.retention_state import (
    RetentionState,
    RetentionWeekData,
)


def retention_cell(
    week_data: rx.Var[RetentionWeekData], index: rx.Var[int]
) -> rx.Component:
    """Renders a single cell in the retention table."""
    percentage = week_data["value"]
    count = week_data["count"]
    base_classes = "p-3 text-center "
    color_class = rx.cond(
        percentage.is_not_none(),
        rx.cond(
            percentage >= 80,
            "bg-blue-600 text-white rounded-lg",
            rx.cond(
                percentage >= 60,
                "bg-blue-500 text-white rounded-lg",
                rx.cond(
                    percentage >= 40,
                    "bg-blue-400 text-gray-800 rounded-lg",
                    rx.cond(
                        percentage >= 20,
                        "bg-blue-300 text-gray-800 rounded-lg",
                        rx.cond(
                            percentage > 0,
                            "bg-blue-200 text-gray-800 rounded-lg",
                            "bg-gray-50 text-gray-400 rounded-lg",
                        ),
                    ),
                ),
            ),
        ),
        "bg-gray-50 text-gray-400",
    )
    return rx.el.td(
        rx.el.div(
            rx.cond(
                percentage.is_not_none(),
                rx.el.div(
                    rx.el.p(
                        percentage.to_string() + "%",
                        class_name="text-sm font-medium",
                    ),
                    rx.el.p(count.to_string(), class_name="text-xs"),
                    class_name="flex flex-col items-center justify-center h-full",
                ),
                rx.el.div(
                    rx.el.p(
                        "-",
                        class_name="text-sm font-medium text-gray-400",
                    ),
                    rx.el.p(
                        "- -",
                        class_name="text-sm font-medium text-gray-400",
                    ),
                    class_name="flex flex-col items-center justify-center h-full",
                ),
            ),
            class_name=base_classes + color_class,
        ),
        class_name="p-[2px]",
    )


def retention_component() -> rx.Component:
    """The Cohort Retention tab UI."""
    return rx.el.div(
        rx.el.h2(
            "Cohort Retention",
            class_name="text-2xl font-semibold text-gray-800 mb-2",
        ),
        rx.el.p(
            "Track customer engagement patterns and analyze support trends across user segments",
            class_name="text-sm text-gray-600 mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.foreach(
                            RetentionState.column_headers,
                            lambda header: rx.el.th(
                                header,
                                scope="col",
                                class_name="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                        ),
                        class_name="border-none",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        RetentionState.retention_data,
                        lambda row_data, index: rx.el.tr(
                            rx.el.td(
                                row_data["cohort"],
                                class_name="px-3 py-3 whitespace-nowrap text-sm font-medium text-gray-900 border-none",
                            ),
                            rx.foreach(
                                row_data["weeks"],
                                lambda week_data, week_index: retention_cell(
                                    week_data, week_index
                                ),
                            ),
                            class_name="border-none",
                        ),
                    ),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full divide-y divide-gray-200 border border-gray-200 shadow-sm rounded-lg overflow-hidden",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="p-6 bg-white rounded-lg shadow",
    )
