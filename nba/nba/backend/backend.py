import csv
import random
from pathlib import Path
from typing import Dict, List

import reflex as rx

from .data_items import all_items
from .player import Player

_CSV_PATH = Path(__file__).resolve().parents[2] / "nbastats.csv"


def _load_players() -> list[Player]:
    """Load the player roster once from the bundled CSV.

    Missing salary/college cells are kept as the string "NaN" to match the
    original pandas-backed behavior (empty cells became NaN floats).

    Returns:
        The full list of players.
    """
    players: list[Player] = []
    with _CSV_PATH.open(newline="") as f:
        for row in csv.DictReader(f):
            salary = row["salary"]
            players.append(
                Player(
                    name=row["name"],
                    team=row["team"],
                    number=int(row["number"]),
                    position=row["position"],
                    age=int(row["age"]),
                    height=row["height"],
                    weight=int(row["weight"]),
                    college=row["college"] or "NaN",
                    salary=int(salary) if salary else "NaN",
                )
            )
    return players


# The roster is identical for every session, so load it once at import time
# and keep it server-side instead of re-reading the CSV and stashing it in
# per-connection state.
PLAYERS: list[Player] = _load_players()

_SEARCH_ATTRS = (
    "name",
    "team",
    "number",
    "position",
    "age",
    "height",
    "weight",
    "college",
    "salary",
)


class State(rx.State):
    """Table-tab state: search, sort and pagination over the roster."""

    search_value: str = ""
    sort_value: str = "name"  # Matches the "Sort By: Name" select default.
    sort_reverse: bool = False

    total_items: int = len(PLAYERS)
    offset: int = 0
    limit: int = 12  # Number of rows per page

    @rx.event
    def set_sort_value(self, value: str):
        self.sort_value = value

    @rx.event
    def set_search_value(self, value: str):
        self.search_value = value

    @rx.var(cache=True)
    def _filtered_sorted_players(self) -> list[Player]:
        # Backend-only (leading underscore): the full filtered list never
        # crosses the wire; only `get_current_page` is sent to the client.
        players = PLAYERS

        if self.sort_value:
            if self.sort_value in ("salary", "number"):
                players = sorted(
                    players,
                    key=lambda player: float(getattr(player, self.sort_value)),
                    reverse=self.sort_reverse,
                )
            else:
                players = sorted(
                    players,
                    key=lambda player: str(getattr(player, self.sort_value)).lower(),
                    reverse=self.sort_reverse,
                )

        if self.search_value:
            search_value = self.search_value.lower()
            players = [
                player
                for player in players
                if any(
                    search_value in str(getattr(player, attr)).lower()
                    for attr in _SEARCH_ATTRS
                )
            ]

        return players

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 0
        )

    @rx.var(cache=True)
    def get_current_page(self) -> list[Player]:
        return self._filtered_sorted_players[self.offset : self.offset + self.limit]

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

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse


class StatsState(rx.State):
    """Stats-tab state: selections, range filters and chart aggregations.

    Kept separate from `State` so none of the chart data is computed or sent
    to the client while the Table tab is showing.
    """

    selected_items: Dict[str, List] = all_items  # All items are selected by default.
    age: tuple[int, int] = (19, 40)
    salary: tuple[int, int] = (0, 25000000)

    stats_view: str = "age_salary"
    radar_toggle: bool = False
    area_toggle: bool = False

    @rx.event
    def set_age(self, value: list[int | float]):
        self.age = (int(value[0]), int(value[1]))

    @rx.event
    def set_salary(self, value: list[int | float]):
        self.salary = (int(value[0]), int(value[1]))

    @rx.event
    def set_stats_view(self, value: str):
        self.stats_view = value

    def toggle_radarchart(self):
        self.radar_toggle = not self.radar_toggle

    def toggle_areachart(self):
        self.area_toggle = not self.area_toggle

    def add_selected(self, list_name: str, item: str):
        self.selected_items[list_name].append(item)

    def remove_selected(self, list_name: str, item: str):
        self.selected_items[list_name].remove(item)

    def add_all_selected(self, list_name: str):
        self.selected_items[list_name] = list(all_items[list_name])

    def clear_selected(self, list_name: str):
        self.selected_items[list_name].clear()

    def random_selected(self, list_name: str):
        items = all_items[list_name]
        self.selected_items[list_name] = random.sample(
            items, random.randint(1, len(items))
        )

    def _passes_filters(self, player: Player) -> bool:
        """Whether a player matches the current team/college/position/age/salary selection.

        Args:
            player: The player to test.

        Returns:
            True if the player should be included in the charts.
        """
        return (
            player.salary != "NaN"
            and player.team in self.selected_items["teams"]
            and player.college in self.selected_items["colleges"]
            and player.position in self.selected_items["positions"]
            and self.age[0] <= player.age <= self.age[1]
            and self.salary[0] <= float(player.salary) <= self.salary[1]
        )

    def _average_by(self, group_attr: str, value_attr: str) -> dict:
        """Average ``value_attr`` over chart-filtered players, grouped by ``group_attr``.

        Args:
            group_attr: Player attribute to group on (e.g. "team", "age").
            value_attr: Player attribute to average within each group.

        Returns:
            Each group value mapped to its rounded average, in first-seen order.
        """
        grouped: dict = {}
        for player in PLAYERS:
            if self._passes_filters(player):
                grouped.setdefault(getattr(player, group_attr), []).append(
                    float(getattr(player, value_attr))
                )
        return {
            key: round(sum(values) / len(values), 2)
            for key, values in grouped.items()
        }

    @rx.var(cache=True)
    def get_age_salary_chart_data(self) -> list[dict]:
        averages = self._average_by("age", "salary")
        return [
            # Include every age in range, even ones with no matching players.
            {"age": age, "average salary": averages.get(age, 0)}
            for age in range(self.age[0], self.age[1] + 1)
        ]

    @rx.var(cache=True)
    def get_position_salary_chart_data(self) -> list[dict]:
        return [
            {"position": position, "average salary": avg}
            for position, avg in self._average_by("position", "salary").items()
        ]

    @rx.var(cache=True)
    def get_team_salary_chart_data(self) -> list[dict]:
        return [
            {"team": team, "average salary": avg}
            for team, avg in self._average_by("team", "salary").items()
        ]

    @rx.var(cache=True)
    def get_college_salary_chart_data(self) -> list[dict]:
        # Players with no college are already dropped by `_passes_filters`
        # (they can't be in the selected colleges list).
        return [
            {"college": college, "average salary": avg}
            for college, avg in self._average_by("college", "salary").items()
        ]

    @rx.var(cache=True)
    def get_team_age_average_data(self) -> list[dict]:
        return [
            {"team": team, "average age": avg}
            for team, avg in self._average_by("team", "age").items()
        ]

    @rx.var(cache=True)
    def get_position_age_average_data(self) -> list[dict]:
        return [
            {"position": position, "average age": avg}
            for position, avg in self._average_by("position", "age").items()
        ]
