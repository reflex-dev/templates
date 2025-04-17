from datetime import datetime
from typing import (
    Dict,
    List,
    Literal,
    Optional,
    TypedDict,
    Union,
)

import reflex as rx

from admin_dashboard.states.initial_data import initial_data


class CustomerData(TypedDict):
    id: int
    customer_name: str
    next_renewal: str
    revenue: float
    licenses: int
    active_licenses: int
    active_license_growth: int
    license_growth: int
    industry: str
    platform: str
    usage_history: List[Dict[str, Union[str, int]]]
    next_renewal_date: Optional[datetime]


def parse_date(date_str: str) -> Optional[datetime]:
    """Parses a date string into a datetime object."""
    try:
        return datetime.strptime(date_str, "%b %d, %Y")
    except ValueError:
        return None


initial_customer_data = initial_data
processed_customers = [
    {
        **customer,
        "next_renewal_date": parse_date(customer["next_renewal"]),
    }
    for customer in initial_customer_data
]
valid_customers = [
    customer
    for customer in processed_customers
    if customer["next_renewal_date"] is not None
]
SortColumn = Literal["next_renewal", "revenue", "licenses", "active_licenses"]
SortOrder = Literal["asc", "desc"]


class DashboardState(rx.State):
    """State for the customer dashboard."""

    customers: List[CustomerData] = valid_customers
    selected_customer_id: Optional[int] = None
    search_term: str = ""
    sort_column: Optional[SortColumn] = "next_renewal"
    sort_order: SortOrder = "asc"
    table_columns: List[str] = [
        "ID",
        "Customer name",
        "Next renewal",
        "Revenue",
        "Licenses",
        "Active licenses",
        "Active license growth",
        "Industry",
        "Platform",
    ]

    @rx.var
    def filtered_customers(self) -> List[CustomerData]:
        """Get customers filtered by search term and sorted."""
        customers_to_filter = list(self.customers)
        if self.search_term:
            search_lower = self.search_term.lower()
            customers_to_filter = [
                customer
                for customer in customers_to_filter
                if search_lower in customer["customer_name"].lower()
            ]
        if self.sort_column is not None:

            def sort_key(customer: CustomerData):
                if self.sort_column == "next_renewal":
                    date_val = customer.get("next_renewal_date")
                    if date_val is None:
                        return (
                            datetime.max if self.sort_order == "asc" else datetime.min
                        )
                    return date_val
                key_value = customer.get(self.sort_column)
                if isinstance(key_value, (int, float)):
                    return key_value
                return float("-inf") if self.sort_order == "asc" else float("inf")

            customers_to_filter = sorted(
                customers_to_filter,
                key=sort_key,
                reverse=self.sort_order == "desc",
            )
        return customers_to_filter

    @rx.var
    def selected_customer(self) -> Optional[CustomerData]:
        """Get the selected customer data."""
        if self.selected_customer_id is None:
            return None
        for customer in self.filtered_customers:
            if customer["id"] == self.selected_customer_id:
                return customer
        for customer in self.customers:
            if customer["id"] == self.selected_customer_id:
                return customer
        return None

    @rx.var
    def result_count(self) -> int:
        """Return the count of filtered results."""
        return len(self.filtered_customers)

    @rx.event
    def select_customer(self, customer_id: int):
        """Select or deselect a customer."""
        if self.selected_customer_id == customer_id:
            self.selected_customer_id = None
        else:
            self.selected_customer_id = customer_id

    @rx.event
    def set_search_term(self, term: str):
        """Set the search term and reset selection."""
        self.search_term = term
        self.selected_customer_id = None

    @rx.event
    def sort_by(self, column_key: SortColumn):
        """Toggle sorting for a specific column."""
        if self.sort_column == column_key:
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
        else:
            self.sort_column = column_key
            self.sort_order = "asc"
        self.selected_customer_id = None
