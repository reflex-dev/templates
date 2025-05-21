from typing import Callable

import reflex as rx
from reflex.event import EventSpec

from retail_dashboard.states.dashboard_state import DashboardState


def filter_checkbox_item(
    label: str,
    is_checked: rx.Var[bool],
    on_change: Callable[[str], None],
    show_flag: bool = False,
) -> rx.Component:
    """Component for a single checkbox item in a filter dropdown."""
    return rx.el.label(
        rx.el.input(
            type="checkbox",
            checked=is_checked,
            on_change=lambda: on_change(label),
            class_name="mr-2.5 h-4 w-4 border-gray-300 rounded text-neutral-600 focus:ring-neutral-500 cursor-pointer",
        ),
        rx.fragment(
            rx.image(
                src=f"https://countryflagsapi.netlify.app/flag/{label}.svg",
                class_name="rounded-[2px] w-4 mr-2.5",
                alt=label + " Flag",
            )
            if show_flag
            else None,
            label,
        ),
        class_name="flex items-center text-sm text-gray-700 p-2.5 hover:bg-gray-50 cursor-pointer rounded-md",
    )


def filter_dropdown_base(
    title: str,
    show_var: rx.Var[bool],
    content: rx.Component,
    reset_action: EventSpec,
    apply_action: EventSpec,
    width_class: str = "w-60",
) -> rx.Component:
    """Base structure for a filter dropdown."""
    return rx.el.div(
        rx.el.p(
            title,
            class_name="text-xs font-medium text-gray-500 px-3 pt-2.5 pb-1.5",
        ),
        content,
        rx.el.div(
            rx.el.button(
                "Reset",
                on_click=reset_action,
                class_name="px-3.5 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg focus:outline-none focus:ring-1 focus:ring-gray-300",
            ),
            rx.el.button(
                "Apply",
                on_click=apply_action,
                class_name="px-3.5 py-2 text-sm text-white bg-neutral-600 hover:bg-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-neutral-500",
            ),
            class_name="flex justify-end space-x-2.5 p-2.5 border-t border-gray-200 bg-gray-50 rounded-b-lg",
        ),
        class_name=f"absolute top-full left-0 mt-2 {width_class} border border-gray-200 rounded-lg z-30 bg-white shadow-lg",
        hidden=~show_var,
    )


def status_filter_dropdown() -> rx.Component:
    """Dropdown component for filtering by Status."""
    content = rx.el.div(
        rx.foreach(
            DashboardState.unique_statuses,
            lambda status: filter_checkbox_item(
                label=status,
                is_checked=DashboardState.temp_selected_statuses.contains(status),
                on_change=DashboardState.toggle_temp_status,
            ),
        ),
        class_name="max-h-48 overflow-y-auto p-2",
    )
    return filter_dropdown_base(
        "Filter by Status",
        DashboardState.show_status_filter,
        content,
        DashboardState.reset_status_filter,
        DashboardState.apply_status_filter,
    )


def country_filter_dropdown() -> rx.Component:
    """Dropdown component for filtering by Country."""
    content = rx.el.div(
        rx.foreach(
            DashboardState.unique_countries,
            lambda country: filter_checkbox_item(
                label=country,
                is_checked=DashboardState.temp_selected_countries.contains(country),
                on_change=DashboardState.toggle_temp_country,
                show_flag=True,
            ),
        ),
        class_name="max-h-48 overflow-y-auto p-2",
    )
    return filter_dropdown_base(
        "Filter by Country",
        DashboardState.show_country_filter,
        content,
        DashboardState.reset_country_filter,
        DashboardState.apply_country_filter,
    )


def costs_filter_dropdown() -> rx.Component:
    """Dropdown component for filtering by Costs."""
    content = rx.el.div(
        rx.el.input(
            placeholder="Min cost",
            on_change=DashboardState.set_temp_min_cost,
            class_name="w-full p-2.5 border border-gray-300 rounded-lg text-sm mb-2.5 focus:outline-none focus:ring-1 focus:ring-neutral-500 focus:border-neutral-500",
            default_value=DashboardState.temp_min_cost_str,
            type="number",
            step="0.01",
        ),
        rx.el.input(
            placeholder="Max cost",
            on_change=DashboardState.set_temp_max_cost,
            class_name="w-full p-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-neutral-500 focus:border-neutral-500",
            default_value=DashboardState.temp_max_cost_str,
            type="number",
            step="0.01",
        ),
        class_name="p-3",
    )
    return filter_dropdown_base(
        "Filter by Costs",
        DashboardState.show_costs_filter,
        content,
        DashboardState.reset_costs_filter,
        DashboardState.apply_costs_filter,
        width_class="w-52",
    )


def filter_button(
    label: str,
    on_click: EventSpec,
    is_active: rx.Var[bool],
    has_filter: rx.Var[bool],
) -> rx.Component:
    """Generic filter button."""
    base_class = "flex items-center px-3.5 py-2 border rounded-lg text-sm font-medium focus:outline-none focus:ring-1 focus:ring-offset-1"
    active_class = f"{base_class} border-neutral-500 bg-neutral-50 text-neutral-700 ring-neutral-400"
    inactive_class = f"{base_class} border-gray-300 text-gray-700 hover:border-gray-400 hover:bg-gray-50 ring-gray-400"
    return rx.el.button(
        rx.el.span(label, class_name="flex items-center"),
        rx.icon(tag="chevron_down", size=16, class_name="ml-2"),
        on_click=on_click,
        class_name=rx.cond(has_filter, active_class, inactive_class),
        aria_expanded=is_active,
    )
