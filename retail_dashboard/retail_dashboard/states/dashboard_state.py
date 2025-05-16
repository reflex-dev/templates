import datetime
import io
from collections import defaultdict
from typing import Dict, List, Optional, Set

import pandas as pd
import reflex as rx

from retail_dashboard.models.entry import DetailEntry
from retail_dashboard.states.data import raw_data


class DashboardState(rx.State):
    """State for the dashboard page."""

    _data: List[DetailEntry] = raw_data
    column_names: List[str] = [
        "Owner",
        "Status",
        "Country",
        "Stability",
        "Costs",
        "Last edited",
    ]
    search_owner: str = ""
    selected_statuses: Set[str] = set()
    selected_countries: Set[str] = set()
    min_cost: Optional[float] = None
    max_cost: Optional[float] = None
    temp_selected_statuses: Set[str] = set()
    temp_selected_countries: Set[str] = set()
    temp_min_cost_str: str = ""
    temp_max_cost_str: str = ""
    show_status_filter: bool = False
    show_country_filter: bool = False
    show_costs_filter: bool = False
    sort_column: Optional[str] = None
    sort_ascending: bool = True
    selected_rows: Set[int] = set()
    current_page: int = 1
    rows_per_page: int = 10

    def _parse_datetime_for_costs(
        self, item: DetailEntry, input_format: str
    ) -> Optional[tuple[datetime.datetime, float]]:
        """Helper to parse datetime and return (datetime, costs) or None on error."""
        try:
            dt_obj = datetime.datetime.strptime(item["last_edited"], input_format)
            return dt_obj, item["costs"]
        except ValueError:
            return None

    @rx.var
    def total_entries_count(self) -> int:
        """Total number of entries in the raw data."""
        return len(self._data)

    @rx.var
    def live_entries_count(self) -> int:
        """Count of 'Live' entries."""
        return sum((1 for item in self._data if item["status"] == "Live"))

    @rx.var
    def inactive_entries_count(self) -> int:
        """Count of 'Inactive' entries."""
        return sum((1 for item in self._data if item["status"] == "Inactive"))

    @rx.var
    def archived_entries_count(self) -> int:
        """Count of 'Archived' entries."""
        return sum((1 for item in self._data if item["status"] == "Archived"))

    @rx.var
    def costs_trend_data(
        self,
    ) -> List[Dict[str, str | float]]:
        """Data for the costs trend line chart."""
        daily_costs = defaultdict(float)

        input_format = "%d/%m/%Y %H:%M"
        output_format = "%Y-%m-%d"
        display_format = "%b %d"

        valid_items = []
        for item in self._data:
            parsed_item = self._parse_datetime_for_costs(item, input_format)
            if parsed_item:
                valid_items.append(parsed_item)

        for dt_obj, cost in valid_items:
            date_str = dt_obj.strftime(output_format)
            daily_costs[date_str] += cost

        sorted_dates = sorted(daily_costs.keys())
        chart_data: List[Dict[str, str | float]] = [
            {
                "date": datetime.datetime.strptime(date_str, output_format).strftime(
                    display_format
                ),
                "total_costs": round(daily_costs[date_str], 2),
            }
            for date_str in sorted_dates
        ]
        return chart_data

    @rx.var
    def recent_activities(self) -> List[DetailEntry]:
        """Get the 5 most recent activities based on last_edited date."""
        # Precompute sort keys to move try-except out of the sorting process itself
        items_with_sort_keys = [
            (self._get_sort_key_for_recent_activities(item), item)
            for item in self._data
        ]

        # Sort based on the precomputed keys
        items_with_sort_keys.sort(key=lambda x: x[0], reverse=True)

        # Extract the original items in sorted order
        sorted_data = [item for _, item in items_with_sort_keys]
        return sorted_data[:5]

    def _get_sort_key_for_recent_activities(
        self, item: DetailEntry
    ) -> datetime.datetime:
        """Helper to get sort key for recent activities, handling potential ValueError."""
        try:
            return datetime.datetime.strptime(item["last_edited"], "%d/%m/%Y %H:%M")
        except ValueError:
            return datetime.datetime.min

    @rx.var
    def unique_statuses(self) -> List[str]:
        """Get unique statuses from the data."""
        return sorted({item["status"] for item in self._data})

    @rx.var
    def unique_countries(self) -> List[str]:
        """Get unique countries from the data."""
        return sorted({item["country"] for item in self._data})

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
        if self.selected_countries:
            data = [item for item in data if item["country"] in self.selected_countries]
        if self.min_cost is not None:
            data = [item for item in data if item["costs"] >= self.min_cost]
        if self.max_cost is not None:
            data = [item for item in data if item["costs"] <= self.max_cost]
        return data

    def _get_sort_key_for_filtered_data(
        self, item: DetailEntry, internal_key: str, is_date_col: bool
    ) -> datetime.datetime | str | int | float:
        """Helper to get sort key for filtered_and_sorted_data."""
        try:
            if is_date_col:
                return datetime.datetime.strptime(item[internal_key], "%d/%m/%Y %H:%M")
            val = item[internal_key]
            if isinstance(val, (int, float)):
                return val
            return str(val).lower()
        except (KeyError, ValueError):
            # Return a value that will sort consistently for error cases
            if is_date_col:
                return datetime.datetime.min
            return ""

    @rx.var
    def filtered_and_sorted_data(self) -> List[DetailEntry]:
        """Sort the filtered data."""
        data_to_sort = self.filtered_data
        if self.sort_column:
            sort_key_map = {
                "Owner": "owner",
                "Status": "status",
                "Country": "country",
                "Stability": "stability",
                "Costs": "costs",
                "Last edited": "last_edited",
            }
            internal_key = sort_key_map.get(self.sort_column)
            if internal_key:
                is_date_col = self.sort_column == "Last edited"

                # Precompute sort keys
                items_with_sort_keys = [
                    (
                        self._get_sort_key_for_filtered_data(
                            item, internal_key, is_date_col
                        ),
                        item,
                    )
                    for item in data_to_sort
                ]

                # Sort based on precomputed keys
                items_with_sort_keys.sort(
                    key=lambda x: x[0], reverse=not self.sort_ascending
                )

                data_to_sort = [item for _, item in items_with_sort_keys]
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
        return f"{start} - {end}"

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

    @rx.event
    def set_search_owner(self, value: str):
        """Update the search owner filter."""
        self.search_owner = value
        self.current_page = 1

    @rx.event
    def toggle_sort(self, column_name: str):
        """Toggle sorting for a column."""
        if self.sort_column == column_name:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = column_name
            self.sort_ascending = True
        self.current_page = 1

    @rx.event
    def go_to_page(self, page_number: int):
        """Navigate to a specific page."""
        if 1 <= page_number <= self.total_pages:
            self.current_page = page_number

    @rx.event
    def next_page(self):
        """Go to the next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1

    @rx.event
    def previous_page(self):
        """Go to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1

    @rx.event
    def toggle_row_selection(self, row_id: int):
        """Toggle selection state for a single row using its ID."""
        if row_id in self.selected_rows:
            self.selected_rows.remove(row_id)
        else:
            self.selected_rows.add(row_id)

    @rx.event
    def toggle_select_all_on_page(self):
        """Select or deselect all rows on the current page."""
        page_ids = self.page_item_ids
        if self.all_rows_on_page_selected:
            self.selected_rows -= page_ids
        else:
            self.selected_rows.update(page_ids)

    @rx.event
    def toggle_status_filter(self):
        """Toggle the visibility of the status filter dropdown."""
        self.show_status_filter = not self.show_status_filter
        if self.show_status_filter:
            self.temp_selected_statuses = self.selected_statuses.copy()
            self.show_country_filter = False
            self.show_costs_filter = False

    @rx.event
    def toggle_country_filter(self):
        """Toggle the visibility of the country filter dropdown."""
        self.show_country_filter = not self.show_country_filter
        if self.show_country_filter:
            self.temp_selected_countries = self.selected_countries.copy()
            self.show_status_filter = False
            self.show_costs_filter = False

    @rx.event
    def toggle_costs_filter(self):
        is_opening = not self.show_costs_filter
        self.show_costs_filter = is_opening
        self.show_status_filter = False
        self.show_country_filter = False
        if is_opening:
            self.temp_min_cost_str = (
                str(self.min_cost) if self.min_cost is not None else ""
            )
            self.temp_max_cost_str = (
                str(self.max_cost) if self.max_cost is not None else ""
            )

    @rx.event
    def toggle_temp_status(self, status: str):
        """Toggle a status in the temporary set."""
        self.temp_selected_statuses.symmetric_difference_update({status})

    @rx.event
    def toggle_temp_country(self, country: str):
        """Toggle a country in the temporary set."""
        self.temp_selected_countries.symmetric_difference_update({country})

    @rx.event
    def set_temp_min_cost(self, value: float):
        self.temp_min_cost_str = str(value) if value is not None else ""

    @rx.event
    def set_temp_max_cost(self, value: float):
        self.temp_max_cost_str = str(value) if value is not None else ""

    @rx.event
    def apply_status_filter(self):
        """Apply the temporary status filter to the main selection."""
        self.selected_statuses = self.temp_selected_statuses.copy()
        self.current_page = 1
        self.close_filter_dropdowns()

    @rx.event
    def apply_country_filter(self):
        """Apply the temporary country filter to the main selection."""
        self.selected_countries = self.temp_selected_countries.copy()
        self.current_page = 1
        self.close_filter_dropdowns()

    @rx.event
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
        if (
            new_min_cost is not None
            and new_max_cost is not None
            and (new_min_cost > new_max_cost)
        ):
            self.min_cost = new_max_cost
            self.max_cost = new_min_cost
        else:
            self.min_cost = new_min_cost
            self.max_cost = new_max_cost
        self.show_costs_filter = False
        self.current_page = 1

    @rx.event
    def reset_status_filter(self):
        """Reset the status filter."""
        self.temp_selected_statuses = set()

    @rx.event
    def reset_country_filter(self):
        """Reset the country filter."""
        self.temp_selected_countries = set()

    @rx.event
    def reset_costs_filter(self):
        self.temp_min_cost_str = ""
        self.temp_max_cost_str = ""
        self.min_cost = None
        self.max_cost = None
        self.show_costs_filter = False
        self.current_page = 1

    @rx.event
    def reset_all_filters(self):
        """Reset all active filters and search."""
        self.search_owner = ""
        self.selected_statuses = set()
        self.selected_countries = set()
        self.min_cost = None
        self.max_cost = None
        self.temp_selected_statuses = set()
        self.temp_selected_countries = set()
        self.temp_min_cost_str = ""
        self.temp_max_cost_str = ""
        self.sort_column = None
        self.current_page = 1
        self.close_filter_dropdowns()

    @rx.event
    def close_filter_dropdowns(self):
        self.show_status_filter = False
        self.show_country_filter = False
        self.show_costs_filter = False

    @rx.event
    def download_csv(self):
        """Download the filtered and sorted data as CSV."""
        if not self.filtered_and_sorted_data:
            return rx.toast("No data to export.", duration=3000)
        df = pd.DataFrame(self.filtered_and_sorted_data)
        column_mapping = {
            "owner": "Owner",
            "status": "Status",
            "country": "Country",
            "stability": "Stability (%)",
            "costs": "Costs ($)",
            "last_edited": "Last Edited",
        }
        df_display_cols = [key for key in column_mapping if key in df.columns]
        df_display = df[df_display_cols]
        df_display = df_display.rename(columns=column_mapping)
        stream = io.StringIO()
        df_display.to_csv(stream, index=False)
        return rx.download(
            data=stream.getvalue(),
            filename="retail_data_export.csv",
        )
