import reflex as rx

from retail_dashboard.states.dashboard_state import DashboardState


def status_badge(status: rx.Var[str]) -> rx.Component:
    """Creates a colored status badge."""
    return rx.el.span(
        rx.el.span(
            class_name=rx.match(
                status,
                (
                    "Live",
                    "h-1.5 w-1.5 rounded-full bg-emerald-500 mr-1.5",
                ),
                (
                    "Inactive",
                    "h-1.5 w-1.5 rounded-full bg-amber-500 mr-1.5",
                ),
                (
                    "Archived",
                    "h-1.5 w-1.5 rounded-full bg-slate-500 mr-1.5",
                ),
                "h-1.5 w-1.5 rounded-full bg-slate-400 mr-1.5",
            )
        ),
        status,
        class_name=rx.match(
            status,
            (
                "Live",
                "inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-emerald-100 text-emerald-700",
            ),
            (
                "Inactive",
                "inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-amber-100 text-amber-700",
            ),
            (
                "Archived",
                "inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-slate-100 text-slate-600",
            ),
            "inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-slate-100 text-slate-600",
        ),
    )


def table_header_cell(name: str) -> rx.Component:
    """Creates a table header cell without sorting functionality."""
    return rx.el.th(
        rx.el.div(
            rx.icon(
                tag=rx.match(
                    name,
                    ("Owner", "user"),
                    ("Status", "bar_chart_horizontal_big"),
                    ("Country", "globe_2"),
                    ("Stability", "trending_up"),
                    ("Costs", "banknote"),
                    ("Last edited", "history"),
                    "table_columns",
                ),
                size=16,
                class_name="mr-2 stroke-neutral-400 group-hover:stroke-neutral-500 size-4",
            ),
            name,
            rx.el.span(class_name="ml-auto"),
            class_name="flex items-center group",
        ),
        scope="col",
        class_name="px-6 py-3.5 text-left text-sm font-medium text-gray-600 uppercase tracking-wider select-none",
    )


def details_table() -> rx.Component:
    """The main table component displaying details."""
    return rx.el.div(
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.foreach(
                            DashboardState.column_names,
                            lambda col_name: table_header_cell(col_name),
                        )
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.paginated_data,
                        lambda row: rx.el.tr(
                            rx.el.td(
                                row["owner"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800",
                            ),
                            rx.el.td(
                                status_badge(row["status"]),
                                class_name="px-6 py-4 whitespace-nowrap text-sm",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.cond(
                                        row["country"],
                                        rx.fragment(
                                            rx.image(
                                                src=f"https://countryflagsapi.netlify.app/flag/{row['country']}.svg",
                                                class_name="rounded-[2px] w-6 mr-2.5",
                                                alt=row["country"] + " Flag",
                                            ),
                                            row["country"],
                                        ),
                                        rx.el.span("", class_name="w-6 mr-2.5"),
                                    ),
                                    class_name="flex items-center",
                                ),
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                            ),
                            rx.el.td(
                                f"{row['stability']}%",
                                class_name=rx.cond(
                                    row["stability"] == 0,
                                    "text-gray-600",
                                    rx.cond(
                                        row["stability"] > 0,
                                        "text-emerald-600",
                                        "text-red-600",
                                    ),
                                )
                                + " px-6 py-4 whitespace-nowrap text-sm",
                            ),
                            rx.el.td(
                                "$"
                                + rx.cond(
                                    row["costs"] == 0,
                                    "0.00",
                                    row["costs"].to_string(),
                                ),
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                            ),
                            rx.el.td(
                                row["last_edited"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                            ),
                            class_name="hover:bg-gray-50/70 border-b border-gray-200/75 last:border-b-0",
                        ),
                    )
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="overflow-x-auto rounded-lg border border-gray-200 bg-white",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Showing "
                    + DashboardState.current_rows_display
                    + " of "
                    + DashboardState.total_rows.to_string(),
                    class_name="text-sm text-gray-600 mr-4",
                ),
                rx.el.button(
                    rx.icon(tag="chevron_left", size=20),
                    on_click=DashboardState.previous_page,
                    disabled=DashboardState.current_page <= 1,
                    class_name="p-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 text-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-gray-300",
                ),
                rx.el.button(
                    rx.icon(tag="chevron_right", size=20),
                    on_click=DashboardState.next_page,
                    disabled=DashboardState.current_page >= DashboardState.total_pages,
                    class_name="p-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 ml-2 text-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-gray-300",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-center sm:justify-end mt-1 md:mt-2 px-2 sm:px-4 py-3.5",
        ),
        class_name="mt-3 md:mt-6",
    )
