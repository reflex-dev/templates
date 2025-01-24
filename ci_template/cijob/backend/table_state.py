import csv
from pathlib import Path
from typing import List

import reflex as rx


class Item(rx.Base):
    """The item class."""

    pipeline: str
    status: str
    workflow: str
    timestamp: str
    duration: str

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return (
                self.pipeline == other.pipeline and
                self.status == other.status and
                self.workflow == other.workflow and
                self.timestamp == other.timestamp and
                self.duration == other.duration
        )

    def __hash__(self):
        return hash((self.pipeline, self.status, self.workflow, self.timestamp, self.duration))


class TableState(rx.State):
    """The state class."""
    initial_items: List[Item] = []
    items: List[Item] = []

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page

    @rx.var(cache=True)
    def filtered_sorted_items(self) -> List[Item]:
        items = self.items

        # Filter items based on selected item
        if self.sort_value:
            items = sorted(
                items,
                key=lambda item: str(getattr(item, self.sort_value)).lower(),
                reverse=self.sort_reverse,
            )

        # Filter items based on search value
        if self.search_value:
            self.offset = 0
            search_value = self.search_value.lower()
            items = [
                item
                for item in items
                if any(
                    search_value in str(getattr(item, attr)).lower()
                    for attr in [
                        "pipeline",
                        "status",
                        "workflow",
                        "timestamp",
                        "duration",
                    ]
                )
            ]

        return items

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        filtered_items_count = len(self.filtered_sorted_items)
        total = (filtered_items_count // self.limit) + (
            1 if filtered_items_count % self.limit else 0
        )
        return total if total > 0 else 1

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> list[Item]:
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_items[start_index:end_index]

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit

    def load_entries(self):
        with Path("data.csv").open(encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.items = [Item(**row) for row in reader]
            self.initial_items = self.items.copy()
            self.total_items = len(self.items)

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    def delete_item(self, item: Item):
        self.items.remove(item)
        self.initial_items.remove(item)
        self.total_items = len(self.items)
        self.first_page()
        return rx.toast.success(f"{item.pipeline} deleted successfully")



