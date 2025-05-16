import reflex as rx

from retail_dashboard.components.details_table import details_table
from retail_dashboard.components.header import header as details_page_header


def details_page_layout() -> rx.Component:
    """The main layout for the Details page."""
    return rx.el.div(
        details_page_header(),
        details_table(),
        class_name="p-2 md:p-6",
    )
