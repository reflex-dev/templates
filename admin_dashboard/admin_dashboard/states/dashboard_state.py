from datetime import datetime
from typing import (
    List,
    Literal,
    Optional,
    Tuple,
)

import reflex as rx

from admin_dashboard.models.models import CustomerData
from admin_dashboard.states.data import initial_customer_data_raw
from admin_dashboard.states.utils import parse_date

SortColumn = Literal[
    "id",
    "next_renewal",
    "revenue",
    "licenses",
    "active_licenses",
]
SortOrder = Literal["asc", "desc"]

processed_customers: List[CustomerData] = [
    {
        **customer,
        "next_renewal_date": parse_date(customer["next_renewal"]),
    }
    for customer in initial_customer_data_raw
]

COLUMN_MAPPING: List[Tuple[str, Optional[SortColumn]]] = [
    ("ID", "id"),
    ("Customer name", None),
    ("Next renewal", "next_renewal"),
    ("Revenue", "revenue"),
    ("Licenses", "licenses"),
    ("Active licenses", "active_licenses"),
    ("Active license growth", None),
    ("Industry", None),
    ("Platform", None),
]


class DashboardState(rx.State):
    """State class managing the customer dashboard data and UI interactions."""

    customers: List[CustomerData] = processed_customers
    selected_customer_id: Optional[int] = None
    search_term: str = ""
    sort_column: Optional[SortColumn] = "id"
    sort_order: SortOrder = "asc"

    @rx.var
    def column_data(
        self,
    ) -> List[Tuple[str, Optional[SortColumn]]]:
        """Returns the master list of column configurations (name and sort key)."""
        return COLUMN_MAPPING

    @rx.var
    def filtered_customers(self) -> List[CustomerData]:
        """Returns the list of customers filtered by search term and sorted according to current settings."""
        customers_to_process = list(self.customers)
        if self.search_term:
            search_lower = self.search_term.lower()
            customers_to_process = [
                customer
                for customer in customers_to_process
                if search_lower in customer["customer_name"].lower()
            ]
        if self.sort_column:

            def get_sort_key(customer: CustomerData):
                sort_key = self.sort_column
                if sort_key == "next_renewal":
                    date_val = customer.get("next_renewal_date")
                    if date_val is None:
                        return (
                            datetime.max if self.sort_order == "asc" else datetime.min
                        )
                    return date_val
                elif sort_key in [
                    "id",
                    "revenue",
                    "licenses",
                    "active_licenses",
                ]:
                    key_value = customer.get(sort_key)
                    return key_value if isinstance(key_value, (int, float)) else 0
                else:
                    return 0

            customers_to_process = sorted(
                customers_to_process,
                key=get_sort_key,
                reverse=self.sort_order == "desc",
            )
        return customers_to_process

    @rx.var
    def selected_customer(self) -> Optional[CustomerData]:
        """Returns the full data dictionary for the currently selected customer, or None if no selection."""
        if self.selected_customer_id is None:
            return None
        for customer in self.customers:
            if customer["id"] == self.selected_customer_id:
                return customer
        return None

    @rx.var
    def result_count(self) -> int:
        """Returns the number of customers currently displayed in the table (after filtering)."""
        return len(self.filtered_customers)

    @rx.event
    def select_customer(self, customer_id: int):
        """Handles clicking on a customer row. Selects the customer or deselects if already selected."""
        if self.selected_customer_id == customer_id:
            self.selected_customer_id = None
        else:
            self.selected_customer_id = customer_id

    @rx.event
    def set_search_term(self, term: str):
        """Updates the search term based on user input."""
        self.search_term = term
        if self.selected_customer_id is not None:
            found = any(
                (
                    customer["id"] == self.selected_customer_id
                    for customer in self.filtered_customers
                )
            )
            if not found:
                self.selected_customer_id = None

    @rx.event
    def sort_by(self, column_key: SortColumn):
        """Handles clicking on a sortable table header. Updates the sort column and order."""
        if self.sort_column == column_key:
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
        else:
            self.sort_column = column_key
            self.sort_order = "asc"
