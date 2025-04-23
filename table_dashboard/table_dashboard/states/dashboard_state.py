import datetime
import io
from typing import (
    List,
    Optional,
    Set,
)

import pandas as pd
import reflex as rx

from table_dashboard.models.entry import DetailEntry
from table_dashboard.states.data import raw_data


class DashboardState(rx.State):
    """State for the dashboard page."""

    _data: List[DetailEntry] = raw_data
    column_names: List[str] = [
        "Owner",
        "Status",
        "Region",
        "Stability",
        "Costs",
        "Last edited",
        "Edit",
    ]
    search_owner: str = ""
    selected_statuses: Set[str] = set()
    selected_regions: Set[str] = set()
    min_cost: Optional[float] = None
    max_cost: Optional[float] = None
    temp_selected_statuses: Set[str] = set()
    temp_selected_regions: Set[str] = set()
    temp_min_cost_str: str = ""
    temp_max_cost_str: str = ""
    show_status_filter: bool = False
    show_region_filter: bool = False
    show_costs_filter: bool = False
    sort_column: Optional[str] = None
    sort_ascending: bool = True
    selected_rows: Set[int] = set()
    current_page: int = 1
    rows_per_page: int = 20

    @rx.var
    def unique_statuses(self) -> List[str]:
        """Get unique statuses from the data."""
        return sorted({item["status"] for item in self._data})

    @rx.var
    def unique_regions(self) -> List[str]:
        """Get unique regions from the data."""
        return sorted({item["region"] for item in self._data})

    @rx.var
    def filtered_data(self) -> List[DetailEntry]:
        """Filter the data based on current filter selections."""
        data = self._data
        if self.search_owner:
            data = [
                item
                for item in data
                if self.search_owner.lower() in item["owner"].lower()
            ]
        if self.selected_statuses:
            data = [item for item in data if item["status"] in self.selected_statuses]
        if self.selected_regions:
            data = [item for item in data if item["region"] in self.selected_regions]
        if self.min_cost is not None:
            data = [item for item in data if item["costs"] >= self.min_cost]
        if self.max_cost is not None:
            data = [item for item in data if item["costs"] <= self.max_cost]
        return data

    @rx.var
    def filtered_and_sorted_data(self) -> List[DetailEntry]:
        """Sort the filtered data."""
        data_to_sort = self.filtered_data
        if self.sort_column:
            try:
                sort_key_map = {
                    "Owner": "owner",
                    "Status": "status",
                    "Region": "region",
                    "Stability": "stability",
                    "Costs": "costs",
                    "Last edited": "last_edited",
                }
                internal_key = sort_key_map.get(self.sort_column)
                if internal_key:
                    if self.sort_column == "Last edited":

                        def key_func(item):
                            return datetime.datetime.strptime(
                                item[internal_key],
                                "%d/%m/%Y %H:%M",
                            )
                    else:

                        def key_func(item):
                            return item[internal_key]

                    data_to_sort = sorted(
                        data_to_sort,
                        key=key_func,
                        reverse=not self.sort_ascending,
                    )
                else:
                    pass
            except KeyError:
                pass
            except ValueError:
                pass
        return data_to_sort

    @rx.var
    def total_rows(self) -> int:
        """Total number of rows after filtering."""
        return len(self.filtered_and_sorted_data)

    @rx.var
    def total_pages(self) -> int:
        """Total number of pages."""
        if self.rows_per_page <= 0:
            return 1
        return (
            (self.total_rows + self.rows_per_page - 1) // self.rows_per_page
            if self.rows_per_page > 0
            else 1
        )

    @rx.var
    def paginated_data(self) -> List[DetailEntry]:
        """Get the data for the current page."""
        start_index = (self.current_page - 1) * self.rows_per_page
        end_index = start_index + self.rows_per_page
        return self.filtered_and_sorted_data[start_index:end_index]

    @rx.var
    def current_rows_display(self) -> str:
        """Display string for current rows."""
        if self.total_rows == 0:
            return "0"
        start = (self.current_page - 1) * self.rows_per_page + 1
        end = min(
            self.current_page * self.rows_per_page,
            self.total_rows,
        )
        return f"{start}-{end}"

    @rx.var
    def page_item_ids(self) -> Set[int]:
        """Get the set of IDs for items on the current page."""
        return {item["id"] for item in self.paginated_data}

    @rx.var
    def all_rows_on_page_selected(self) -> bool:
        """Check if all rows on the current page are selected."""
        if not self.paginated_data:
            return False
        return self.page_item_ids.issubset(self.selected_rows)

    def set_search_owner(self, value: str):
        """Update the search owner filter."""
        self.search_owner = value
        self.current_page = 1

    def toggle_sort(self, column_name: str):
        """Toggle sorting for a column."""
        if self.sort_column == column_name:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = column_name
            self.sort_ascending = True

    def go_to_page(self, page_number: int):
        """Navigate to a specific page."""
        if 1 <= page_number <= self.total_pages:
            self.current_page = page_number

    def next_page(self):
        """Go to the next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1

    def previous_page(self):
        """Go to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1

    def toggle_row_selection(self, row_id: int):
        """Toggle selection state for a single row using its ID."""
        if row_id in self.selected_rows:
            self.selected_rows.remove(row_id)
        else:
            self.selected_rows.add(row_id)

    def toggle_select_all_on_page(self):
        """Select or deselect all rows on the current page."""
        page_ids = self.page_item_ids
        if self.all_rows_on_page_selected:
            self.selected_rows -= page_ids
        else:
            self.selected_rows.update(page_ids)

    def toggle_status_filter(self):
        is_opening = not self.show_status_filter
        self.show_status_filter = is_opening
        self.show_region_filter = False
        self.show_costs_filter = False
        if is_opening:
            self.temp_selected_statuses = self.selected_statuses.copy()

    def toggle_region_filter(self):
        is_opening = not self.show_region_filter
        self.show_region_filter = is_opening
        self.show_status_filter = False
        self.show_costs_filter = False
        if is_opening:
            self.temp_selected_regions = self.selected_regions.copy()

    def toggle_costs_filter(self):
        is_opening = not self.show_costs_filter
        self.show_costs_filter = is_opening
        self.show_status_filter = False
        self.show_region_filter = False
        if is_opening:
            self.temp_min_cost_str = (
                str(self.min_cost) if self.min_cost is not None else ""
            )
            self.temp_max_cost_str = (
                str(self.max_cost) if self.max_cost is not None else ""
            )

    def toggle_temp_status(self, status: str):
        if status in self.temp_selected_statuses:
            self.temp_selected_statuses.remove(status)
        else:
            self.temp_selected_statuses.add(status)

    def toggle_temp_region(self, region: str):
        if region in self.temp_selected_regions:
            self.temp_selected_regions.remove(region)
        else:
            self.temp_selected_regions.add(region)

    def set_temp_min_cost(self, value: str):
        self.temp_min_cost_str = value

    def set_temp_max_cost(self, value: str):
        self.temp_max_cost_str = value

    def apply_status_filter(self):
        self.selected_statuses = self.temp_selected_statuses.copy()
        self.show_status_filter = False
        self.current_page = 1

    def apply_region_filter(self):
        self.selected_regions = self.temp_selected_regions.copy()
        self.show_region_filter = False
        self.current_page = 1

    def apply_costs_filter(self):
        new_min_cost = None
        new_max_cost = None
        try:
            if self.temp_min_cost_str:
                new_min_cost = float(self.temp_min_cost_str)
        except ValueError:
            pass
        try:
            if self.temp_max_cost_str:
                new_max_cost = float(self.temp_max_cost_str)
        except ValueError:
            pass
        self.min_cost = new_min_cost
        self.max_cost = new_max_cost
        self.show_costs_filter = False
        self.current_page = 1

    def reset_status_filter(self):
        self.temp_selected_statuses = set()
        self.selected_statuses = set()
        self.show_status_filter = False
        self.current_page = 1

    def reset_region_filter(self):
        self.temp_selected_regions = set()
        self.selected_regions = set()
        self.show_region_filter = False
        self.current_page = 1

    def reset_costs_filter(self):
        self.temp_min_cost_str = ""
        self.temp_max_cost_str = ""
        self.min_cost = None
        self.max_cost = None
        self.show_costs_filter = False
        self.current_page = 1

    def reset_all_filters(self):
        """Reset all filters and search."""
        self.search_owner = ""
        self.selected_statuses = set()
        self.selected_regions = set()
        self.min_cost = None
        self.max_cost = None
        self.temp_selected_statuses = set()
        self.temp_selected_regions = set()
        self.temp_min_cost_str = ""
        self.temp_max_cost_str = ""
        self.show_status_filter = False
        self.show_region_filter = False
        self.show_costs_filter = False
        self.current_page = 1
        self.selected_rows = set()
        self.sort_column = None
        self.sort_ascending = True

    def close_filter_dropdowns(self):
        self.show_status_filter = False
        self.show_region_filter = False
        self.show_costs_filter = False

    @rx.event
    def download_csv(self):
        """Download the filtered and sorted data as CSV."""
        df = pd.DataFrame(self.filtered_and_sorted_data)
        display_columns = [
            col.lower().replace(" ", "_") for col in self.column_names if col != "Edit"
        ]
        if "last_edited" not in df.columns and "last_edited" in display_columns:
            display_columns.remove("last_edited")
        if "costs" in df.columns and "costs" in display_columns:
            pass
        column_mapping = {
            "owner": "Owner",
            "status": "Status",
            "region": "Region",
            "stability": "Stability",
            "costs": "Costs",
            "last_edited": "Last edited",
        }
        df_display = df[[key for key in column_mapping if key in df.columns]]
        df_display.columns = [column_mapping[col] for col in df_display.columns]
        stream = io.StringIO()
        df_display.to_csv(stream, index=False)
        return rx.download(
            data=stream.getvalue(),
            filename="details_export.csv",
        )
