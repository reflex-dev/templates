import reflex as rx

from retention_dashboard.components.charts import donut_chart
from retention_dashboard.states.workflow_state import WorkflowState


def workflow_component() -> rx.Component:
    """The Workflow tab UI."""
    return rx.el.div(
        rx.el.h2(
            "Workflow",
            class_name="text-2xl font-semibold text-gray-800 mb-2",
        ),
        rx.el.p(
            "Analyze case testing efficiency and simulate cost impacts across departments",
            class_name="text-sm text-gray-600 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Test Quota (%)",
                    class_name="block text-sm font-medium text-gray-700 mb-2",
                ),
                rx.el.input(
                    type="range",
                    min="0",
                    max="100",
                    default_value=WorkflowState.test_quota.to_string(),
                    on_change=WorkflowState.set_test_quota,
                    class_name="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600",
                ),
                rx.el.div(
                    rx.el.span(
                        "Current: " + WorkflowState.test_quota.to_string() + "%",
                        class_name="text-xs text-gray-500",
                    ),
                    rx.el.span(
                        "Scenario: " + WorkflowState.test_quota.to_string() + "%",
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="flex justify-between mt-1",
                ),
                class_name="w-full md:w-1/3 pr-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Select department to exclude",
                    class_name="block text-sm font-medium text-gray-700 mb-2",
                ),
                rx.el.div(
                    rx.foreach(
                        WorkflowState.departments,
                        lambda dept: rx.el.label(
                            rx.el.input(
                                type="checkbox",
                                checked=WorkflowState.excluded_departments[dept],
                                on_change=lambda: WorkflowState.toggle_department(dept),
                                class_name="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer",
                            ),
                            dept,
                            class_name="flex items-center text-sm text-gray-700 mr-4 mb-2 cursor-pointer",
                        ),
                    ),
                    class_name="flex flex-wrap",
                ),
                class_name="w-full md:w-2/3 pl-4 mt-4 md:mt-0",
            ),
            class_name="flex flex-col md:flex-row mb-8 p-6 bg-gray-50 rounded-lg border border-gray-200",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "1. Completed Cases",
                    class_name="text-lg font-medium text-gray-700 mb-4 text-center",
                ),
                donut_chart(
                    data=WorkflowState.completed_cases_data,
                    data_key="value",
                    name_key="name",
                    title="",
                    total_value=WorkflowState.completed_cases_data[0]["value"],
                    percentage=WorkflowState.completed_cases_data[0]["percentage"],
                ),
                class_name="w-full md:w-1/3 p-4 border-r border-gray-200",
            ),
            rx.el.div(
                rx.el.h3(
                    "2. Test Results",
                    class_name="text-lg font-medium text-gray-700 mb-4 text-center",
                ),
                donut_chart(
                    data=WorkflowState.test_results_data_tested,
                    data_key="value",
                    name_key="name",
                    title="Tested Cases",
                    total_value=WorkflowState.test_results_data_tested[0]["value"],
                    percentage=WorkflowState.test_results_data_tested[0]["percentage"],
                ),
                rx.el.div(class_name="my-4"),
                donut_chart(
                    data=WorkflowState.test_results_data_untested,
                    data_key="value",
                    name_key="name",
                    title="Untested Cases",
                    total_value=WorkflowState.test_results_data_untested[0]["value"],
                    percentage=WorkflowState.test_results_data_untested[0][
                        "percentage"
                    ],
                ),
                class_name="w-full md:w-1/3 p-4 border-r border-gray-200",
            ),
            rx.el.div(
                rx.el.h3(
                    "3. Impact",
                    class_name="text-lg font-medium text-gray-700 mb-4 text-center",
                ),
                donut_chart(
                    data=WorkflowState.impact_data_error_free,
                    data_key="value",
                    name_key="name",
                    title="Error-free Cases",
                    total_value=WorkflowState.impact_data_error_free[0]["value"],
                    percentage=WorkflowState.impact_data_error_free[0]["percentage"],
                ),
                rx.el.div(class_name="my-4"),
                donut_chart(
                    data=WorkflowState.impact_data_corrected,
                    data_key="value",
                    name_key="name",
                    title="Corrected Cases",
                    total_value=WorkflowState.impact_data_corrected[0]["value"],
                    percentage=WorkflowState.impact_data_corrected[0]["percentage"],
                ),
                class_name="w-full md:w-1/3 p-4",
            ),
            class_name="flex flex-col md:flex-row",
        ),
        class_name="p-6 bg-white rounded-lg shadow",
    )
