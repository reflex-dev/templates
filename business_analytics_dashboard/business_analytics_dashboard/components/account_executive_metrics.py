import reflex as rx

from business_analytics_dashboard.states.dashboard_state import DashboardState


def pagination_controls() -> rx.Component:
    """Component for table pagination controls."""
    return rx.el.div(
        rx.el.span(
            f"Page {DashboardState.current_page} of {DashboardState.total_pages}",
            class_name="text-sm text-gray-700 mr-4",
        ),
        rx.el.button(
            "Previous",
            on_click=DashboardState.previous_page,
            disabled=DashboardState.current_page <= 1,
            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-l-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
        ),
        rx.el.button(
            "Next",
            on_click=DashboardState.next_page,
            disabled=DashboardState.current_page >= DashboardState.total_pages,
            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border-t border-b border-r border-gray-300 rounded-r-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
        ),
        class_name="flex justify-end items-center mt-4",
    )


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
                    rx.el.option("All", value="All"),
                    rx.foreach(
                        DashboardState.departments_for_filter,
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
                default_value=DashboardState.search_query,
                on_change=DashboardState.set_search_query.debounce(300),
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
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "ID",
                                    class_name="p-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 bg-gray-50 border-b",
                                ),
                                rx.el.th(
                                    "First Name",
                                    class_name="p-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 bg-gray-50 border-b",
                                ),
                                rx.el.th(
                                    "Last Name",
                                    class_name="p-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 bg-gray-50 border-b",
                                ),
                                rx.el.th(
                                    "Email",
                                    class_name="p-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 bg-gray-50 border-b",
                                ),
                                rx.el.th(
                                    "Department",
                                    class_name="p-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 bg-gray-50 border-b",
                                ),
                                rx.el.th(
                                    "Salary",
                                    class_name="p-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 bg-gray-50 border-b",
                                ),
                                rx.el.th(
                                    "Projects Closed",
                                    class_name="p-3 text-center text-xs font-semibold uppercase tracking-wider text-gray-500 bg-gray-50 border-b",
                                ),
                                rx.el.th(
                                    "Pending Projects",
                                    class_name="p-3 text-center text-xs font-semibold uppercase tracking-wider text-gray-500 bg-gray-50 border-b",
                                ),
                                class_name="bg-gray-50",
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                DashboardState.paginated_employees,
                                lambda employee: rx.el.tr(
                                    rx.el.td(
                                        employee["employee_id"],
                                        class_name="p-3 border-b text-sm text-gray-700",
                                    ),
                                    rx.el.td(
                                        employee["first_name"],
                                        class_name="p-3 border-b text-sm text-gray-700",
                                    ),
                                    rx.el.td(
                                        employee["last_name"],
                                        class_name="p-3 border-b text-sm text-gray-700",
                                    ),
                                    rx.el.td(
                                        employee["email"],
                                        class_name="p-3 border-b text-sm text-gray-700",
                                    ),
                                    rx.el.td(
                                        employee["department"],
                                        class_name="p-3 border-b text-sm text-gray-700",
                                    ),
                                    rx.el.td(
                                        "$ " + employee["salary"].to_string(),
                                        class_name="p-3 border-b text-sm text-gray-700",
                                    ),
                                    rx.el.td(
                                        employee["projects_closed"],
                                        class_name="p-3 border-b text-sm text-gray-700 text-center",
                                    ),
                                    rx.el.td(
                                        employee["pending_projects"],
                                        class_name="p-3 border-b text-sm text-gray-700 text-center",
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
                                        (DashboardState.search_query != "")
                                        | (DashboardState.selected_department != "All"),
                                        "No employees match your search or filter.",
                                        "No employee data available.",
                                    ),
                                    class_name="text-center text-gray-500 py-4",
                                ),
                                class_name="caption-bottom",
                            ),
                            rx.fragment(),
                        ),
                        class_name="w-full border-collapse bg-white rounded-t-lg shadow-md overflow-hidden",
                    ),
                    rx.cond(
                        ~DashboardState.loading & (DashboardState.total_pages > 1),
                        pagination_controls(),
                        rx.fragment(),
                    ),
                    class_name="overflow-x-auto shadow rounded-lg border border-gray-200",
                ),
            )
        ),
        class_name="bg-white p-6 rounded-lg shadow-md",
    )
