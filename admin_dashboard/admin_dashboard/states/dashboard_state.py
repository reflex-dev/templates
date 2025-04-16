import reflex as rx
from typing import (
    TypedDict,
    Optional,
    List,
    Dict,
    Union,
    Literal,
)
from datetime import datetime


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


initial_customer_data = [
    {
        "id": 1,
        "customer_name": "ABC Company",
        "next_renewal": "Dec 31, 2023",
        "revenue": 600000,
        "licenses": 50,
        "active_licenses": 45,
        "active_license_growth": 65,
        "license_growth": 30,
        "industry": "Finance",
        "platform": "Windows",
        "usage_history": [
            {"month": "Jan", "usage": 40},
            {"month": "Feb", "usage": 42},
            {"month": "Mar", "usage": 41},
            {"month": "Apr", "usage": 43},
            {"month": "May", "usage": 45},
            {"month": "Jun", "usage": 44},
        ],
    },
    {
        "id": 2,
        "customer_name": "XYZ Corporation",
        "next_renewal": "Jan 15, 2024",
        "revenue": 50000,
        "licenses": 25,
        "active_licenses": 20,
        "active_license_growth": -32,
        "license_growth": -10,
        "industry": "Healthcare",
        "platform": "macOS",
        "usage_history": [
            {"month": "Jan", "usage": 15},
            {"month": "Feb", "usage": 16},
            {"month": "Mar", "usage": 18},
            {"month": "Apr", "usage": 17},
            {"month": "May", "usage": 20},
            {"month": "Jun", "usage": 19},
        ],
    },
    {
        "id": 3,
        "customer_name": "123 Enterprises",
        "next_renewal": "Nov 30, 2023",
        "revenue": 75000,
        "licenses": 30,
        "active_licenses": 28,
        "active_license_growth": 90,
        "license_growth": 75,
        "industry": "Education",
        "platform": "macOS",
        "usage_history": [
            {"month": "Jan", "usage": 22},
            {"month": "Feb", "usage": 24},
            {"month": "Mar", "usage": 25},
            {"month": "Apr", "usage": 26},
            {"month": "May", "usage": 28},
            {"month": "Jun", "usage": 27},
        ],
    },
    {
        "id": 4,
        "customer_name": "DEF Inc.",
        "next_renewal": "Feb 28, 2024",
        "revenue": 25000,
        "licenses": 10,
        "active_licenses": 8,
        "active_license_growth": 67,
        "license_growth": 25,
        "industry": "Finance",
        "platform": "Windows",
        "usage_history": [
            {"month": "Jan", "usage": 5},
            {"month": "Feb", "usage": 6},
            {"month": "Mar", "usage": 7},
            {"month": "Apr", "usage": 6},
            {"month": "May", "usage": 8},
            {"month": "Jun", "usage": 7},
        ],
    },
    {
        "id": 5,
        "customer_name": "GHI Corporation",
        "next_renewal": "Dec 15, 2023",
        "revenue": 1000000,
        "licenses": 100,
        "active_licenses": 95,
        "active_license_growth": 30,
        "license_growth": 60,
        "industry": "Healthcare",
        "platform": "macOS",
        "usage_history": [
            {"month": "Jan", "usage": 80},
            {"month": "Feb", "usage": 85},
            {"month": "Mar", "usage": 88},
            {"month": "Apr", "usage": 90},
            {"month": "May", "usage": 95},
            {"month": "Jun", "usage": 92},
        ],
    },
    {
        "id": 6,
        "customer_name": "456 Enterprises",
        "next_renewal": "Jan 31, 2024",
        "revenue": 50000,
        "licenses": 20,
        "active_licenses": 18,
        "active_license_growth": 10,
        "license_growth": -40,
        "industry": "Education",
        "platform": "Windows",
        "usage_history": [
            {"month": "Jan", "usage": 12},
            {"month": "Feb", "usage": 14},
            {"month": "Mar", "usage": 15},
            {"month": "Apr", "usage": 16},
            {"month": "May", "usage": 18},
            {"month": "Jun", "usage": 17},
        ],
    },
    {
        "id": 7,
        "customer_name": "JKL Inc.",
        "next_renewal": "Nov 15, 2023",
        "revenue": 75000,
        "licenses": 30,
        "active_licenses": 25,
        "active_license_growth": -50,
        "license_growth": -30,
        "industry": "Finance",
        "platform": "Windows",
        "usage_history": [
            {"month": "Jan", "usage": 20},
            {"month": "Feb", "usage": 21},
            {"month": "Mar", "usage": 22},
            {"month": "Apr", "usage": 23},
            {"month": "May", "usage": 25},
            {"month": "Jun", "usage": 24},
        ],
    },
    {
        "id": 8,
        "customer_name": "MNO Corporation",
        "next_renewal": "Feb 15, 2024",
        "revenue": 100000,
        "licenses": 50,
        "active_licenses": 48,
        "active_license_growth": 45,
        "license_growth": 60,
        "industry": "Healthcare",
        "platform": "macOS",
        "usage_history": [
            {"month": "Jan", "usage": 40},
            {"month": "Feb", "usage": 42},
            {"month": "Mar", "usage": 44},
            {"month": "Apr", "usage": 45},
            {"month": "May", "usage": 48},
            {"month": "Jun", "usage": 47},
        ],
    },
    {
        "id": 9,
        "customer_name": "789 Enterprises",
        "next_renewal": "Dec 31, 2023",
        "revenue": 25000,
        "licenses": 10,
        "active_licenses": 9,
        "active_license_growth": 80,
        "license_growth": 50,
        "industry": "Education",
        "platform": "iOS",
        "usage_history": [
            {"month": "Jan", "usage": 6},
            {"month": "Feb", "usage": 7},
            {"month": "Mar", "usage": 8},
            {"month": "Apr", "usage": 7},
            {"month": "May", "usage": 9},
            {"month": "Jun", "usage": 8},
        ],
    },
    {
        "id": 10,
        "customer_name": "PQR Inc.",
        "next_renewal": "Jan 31, 2024",
        "revenue": 60000,
        "licenses": 20,
        "active_licenses": 19,
        "active_license_growth": 95,
        "license_growth": 80,
        "industry": "Finance",
        "platform": "iOS",
        "usage_history": [
            {"month": "Jan", "usage": 15},
            {"month": "Feb", "usage": 16},
            {"month": "Mar", "usage": 17},
            {"month": "Apr", "usage": 18},
            {"month": "May", "usage": 19},
            {"month": "Jun", "usage": 18},
        ],
    },
    {
        "id": 11,
        "customer_name": "STU Corporation",
        "next_renewal": "Nov 30, 2023",
        "revenue": 700500,
        "licenses": 30,
        "active_licenses": 27,
        "active_license_growth": 125,
        "license_growth": 30,
        "industry": "Healthcare",
        "platform": "macOS",
        "usage_history": [
            {"month": "Jan", "usage": 20},
            {"month": "Feb", "usage": 22},
            {"month": "Mar", "usage": 23},
            {"month": "Apr", "usage": 25},
            {"month": "May", "usage": 27},
            {"month": "Jun", "usage": 26},
        ],
    },
    {
        "id": 12,
        "customer_name": "DEF Enterprises",
        "next_renewal": "Feb 28, 2024",
        "revenue": 1000000,
        "licenses": 100,
        "active_licenses": 90,
        "active_license_growth": 50,
        "license_growth": 60,
        "industry": "Education",
        "platform": "iOS",
        "usage_history": [
            {"month": "Jan", "usage": 75},
            {"month": "Feb", "usage": 80},
            {"month": "Mar", "usage": 82},
            {"month": "Apr", "usage": 85},
            {"month": "May", "usage": 90},
            {"month": "Jun", "usage": 88},
        ],
    },
    {
        "id": 13,
        "customer_name": "VWX Inc.",
        "next_renewal": "Dec 15, 2023",
        "revenue": 50000,
        "licenses": 25,
        "active_licenses": 23,
        "active_license_growth": 35,
        "license_growth": 80,
        "industry": "Finance",
        "platform": "Windows",
        "usage_history": [
            {"month": "Jan", "usage": 18},
            {"month": "Feb", "usage": 19},
            {"month": "Mar", "usage": 20},
            {"month": "Apr", "usage": 21},
            {"month": "May", "usage": 23},
            {"month": "Jun", "usage": 22},
        ],
    },
    {
        "id": 14,
        "customer_name": "YZA Corporation",
        "next_renewal": "Jan 15, 2024",
        "revenue": 75000,
        "licenses": 30,
        "active_licenses": 29,
        "active_license_growth": 25,
        "license_growth": 30,
        "industry": "Healthcare",
        "platform": "macOS",
        "usage_history": [
            {"month": "Jan", "usage": 24},
            {"month": "Feb", "usage": 25},
            {"month": "Mar", "usage": 26},
            {"month": "Apr", "usage": 27},
            {"month": "May", "usage": 29},
            {"month": "Jun", "usage": 28},
        ],
    },
    {
        "id": 15,
        "customer_name": "BCD Enterprises",
        "next_renewal": "Nov 15, 2023",
        "revenue": 25000,
        "licenses": 10,
        "active_licenses": 7,
        "active_license_growth": 10,
        "license_growth": 20,
        "industry": "Education",
        "platform": "Windows",
        "usage_history": [
            {"month": "Jan", "usage": 4},
            {"month": "Feb", "usage": 5},
            {"month": "Mar", "usage": 6},
            {"month": "Apr", "usage": 5},
            {"month": "May", "usage": 7},
            {"month": "Jun", "usage": 6},
        ],
    },
]
processed_customers = [
    {
        **customer,
        "next_renewal_date": parse_date(
            customer["next_renewal"]
        ),
    }
    for customer in initial_customer_data
]
valid_customers = [
    customer
    for customer in processed_customers
    if customer["next_renewal_date"] is not None
]
SortColumn = Literal[
    "next_renewal", "revenue", "licenses", "active_licenses"
]
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
                if search_lower
                in customer["customer_name"].lower()
            ]
        if self.sort_column is not None:

            def sort_key(customer: CustomerData):
                if self.sort_column == "next_renewal":
                    date_val = customer.get(
                        "next_renewal_date"
                    )
                    if date_val is None:
                        return (
                            datetime.max
                            if self.sort_order == "asc"
                            else datetime.min
                        )
                    return date_val
                key_value = customer.get(self.sort_column)
                if isinstance(key_value, (int, float)):
                    return key_value
                return (
                    float("-inf")
                    if self.sort_order == "asc"
                    else float("inf")
                )

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
            self.sort_order = (
                "desc"
                if self.sort_order == "asc"
                else "asc"
            )
        else:
            self.sort_column = column_key
            self.sort_order = "asc"
        self.selected_customer_id = None