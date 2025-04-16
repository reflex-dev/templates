import reflex as rx

from business_analytics_dashboard.states.dashboard_state import DashboardState


def account_executive_metrics_table() -> rx.Component:
    """Table displaying account executive metrics (employee data)."""
    return rx.el.div(
        rx.el.h2(
            "Account Executive Metrics",
            class_name="text-2xl font-semibold text-gray-800 mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Filter by Department:",
                    html_for="department-select",
                    class_name="text-sm font-medium text-gray-700 mr-2",
                ),
                rx.el.select(
                    rx.foreach(
                        DashboardState.available_departments,
                        lambda dept: rx.el.option(dept, value=dept),
                    ),
                    id="department-select",
                    value=DashboardState.selected_department,
                    on_change=DashboardState.set_selected_department,
                    class_name="p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-900",
                ),
                class_name="flex items-center",
            ),
            rx.el.input(
                type="text",
                placeholder="Search in table...",
                on_change=DashboardState.set_search_query.debounce(500),
                class_name="w-full md:w-auto p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-900 placeholder-gray-400",
            ),
            class_name="flex flex-col md:flex-row justify-between items-center mb-6 space-y-4 md:space-y-0",
        ),
        rx.el.div(
            rx.cond(
                DashboardState.loading,
                rx.el.div(
                    rx.el.p(
                        "Loading employee data...",
                        class_name="text-center text-gray-500 py-4",
                    ),
                    class_name="w-full",
                ),
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "ID",
                                class_name="p-3 text-left text-sm font-semibold text-gray-600 bg-gray-100 border-b",
                            ),
                            rx.el.th(
                                "First Name",
                                class_name="p-3 text-left text-sm font-semibold text-gray-600 bg-gray-100 border-b",
                            ),
                            rx.el.th(
                                "Last Name",
                                class_name="p-3 text-left text-sm font-semibold text-gray-600 bg-gray-100 border-b",
                            ),
                            rx.el.th(
                                "Email",
                                class_name="p-3 text-left text-sm font-semibold text-gray-600 bg-gray-100 border-b",
                            ),
                            rx.el.th(
                                "Department",
                                class_name="p-3 text-left text-sm font-semibold text-gray-600 bg-gray-100 border-b",
                            ),
                            class_name="bg-gray-50",
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            DashboardState.filtered_employees,
                            lambda employee: rx.el.tr(
                                rx.el.td(
                                    employee["employee_id"],
                                    class_name="p-3 border-b text-gray-700",
                                ),
                                rx.el.td(
                                    employee["first_name"],
                                    class_name="p-3 border-b text-gray-700",
                                ),
                                rx.el.td(
                                    employee["last_name"],
                                    class_name="p-3 border-b text-gray-700",
                                ),
                                rx.el.td(
                                    employee["email"],
                                    class_name="p-3 border-b text-gray-700",
                                ),
                                rx.el.td(
                                    employee["department"],
                                    class_name="p-3 border-b text-gray-700",
                                ),
                                class_name="hover:bg-gray-50 transition-colors",
                            ),
                        )
                    ),
                    rx.cond(
                        ~DashboardState.loading
                        & (DashboardState.filtered_employees.length() == 0),
                        rx.el.caption(
                            rx.el.p(
                                rx.cond(
                                    DashboardState.search_query != "",
                                    "No employees match your search or filter.",
                                    rx.cond(
                                        DashboardState.selected_department != "All",
                                        "No employees found in the selected department.",
                                        "No employee data available.",
                                    ),
                                ),
                                class_name="text-center text-gray-500 py-4",
                            ),
                            class_name="caption-bottom",
                        ),
                        rx.fragment(),
                    ),
                    class_name="w-full border-collapse bg-white rounded-lg shadow-md overflow-hidden",
                ),
            ),
            class_name="overflow-x-auto shadow rounded-lg border border-gray-200",
        ),
        class_name="bg-white p-6 rounded-lg",
    )
