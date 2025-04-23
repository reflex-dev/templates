import asyncio
import datetime
import random
from typing import List, Literal

import reflex as rx

from stock_market_dashboard.models.models import (
    ChartDataPoint,
    Option,
    Order,
    Position,
    StockInfo,
)
from stock_market_dashboard.states.data import (
    options_calls_data,
    options_puts_data,
    positions_data,
    recent_orders_data,
    stock_info_data,
)


class TradingState(rx.State):
    stock_info: StockInfo = stock_info_data
    chart_data: list[ChartDataPoint] = []
    options_calls: list[Option] = options_calls_data
    options_puts: list[Option] = options_puts_data
    recent_orders: list[Order] = recent_orders_data
    positions: list[Position] = positions_data
    active_main_tab: str = "Options trading"
    active_sub_tab: str = "4D Fri Oct 18"
    running_simulation: bool = False

    @rx.var
    def combined_options(
        self,
    ) -> List[dict[str, dict[str, int]]]:
        """Combine call and put options based on strike price."""
        calls_by_strike = {opt["strike"]: opt for opt in self.options_calls}
        puts_by_strike = {opt["strike"]: opt for opt in self.options_puts}
        all_strikes = sorted(set(calls_by_strike.keys()) | set(puts_by_strike.keys()))
        combined = [
            {
                "call": calls_by_strike.get(strike),
                "put": puts_by_strike.get(strike),
                "strike": strike,
            }
            for strike in all_strikes
        ]

        return combined

    def _generate_initial_chart_data(self):
        """Generates some initial random chart data."""
        if not self.chart_data:
            now = datetime.datetime.now(datetime.timezone.utc)
            start_price = self.stock_info["price"]
            data = []
            for i in range(60):
                time = now - datetime.timedelta(minutes=59 - i)
                price_change = random.uniform(-0.5, 0.5)
                new_price = max(0.1, start_price + price_change)
                data.append(
                    {
                        "time": time.strftime("%H:%M"),
                        "price": round(new_price, 2),
                    }
                )
                start_price = new_price
            self.chart_data = data

    def _update_data_simulation(self):
        """Simulates live data updates."""
        price_change = random.uniform(-0.2, 0.2)
        old_price = self.stock_info["price"]
        new_price = round(max(0.1, old_price + price_change), 2)
        self.stock_info["price"] = new_price
        self.stock_info["change"] = round(new_price - self.stock_info["close"], 2)
        self.stock_info["change_percent"] = (
            round(
                self.stock_info["change"] / self.stock_info["close"] * 100,
                2,
            )
            if self.stock_info["close"]
            else 0
        )
        now = datetime.datetime.now(datetime.timezone.utc)
        self.chart_data.append(
            {
                "time": now.strftime("%H:%M"),
                "price": new_price,
            }
        )
        if len(self.chart_data) > 60:
            self.chart_data.pop(0)
        if self.recent_orders:
            order_index = random.randint(0, len(self.recent_orders) - 1)
            statuses: List[
                Literal[
                    "Sending",
                    "Working",
                    "Filled",
                    "Canceled",
                ]
            ] = ["Sending", "Working", "Filled", "Canceled"]
            if (
                self.recent_orders[order_index]["status"] not in ["Filled", "Canceled"]
                or random.random() < 0.1
            ):
                self.recent_orders[order_index]["status"] = random.choice(statuses)
        if self.positions:
            position_index = random.randint(0, len(self.positions) - 1)
            change_factor = random.uniform(0.995, 1.005)
            old_mkt_val = self.positions[position_index]["mkt_val"]
            new_mkt_val = round(old_mkt_val * change_factor, 2)
            self.positions[position_index]["mkt_val"] = new_mkt_val
            day_return_change = (new_mkt_val - old_mkt_val) * random.uniform(0.8, 1.2)
            self.positions[position_index]["day_return"] = round(
                self.positions[position_index]["day_return"] + day_return_change,
                2,
            )
            self.positions[position_index]["total_ret"] = round(
                self.positions[position_index]["total_ret"] + day_return_change,
                2,
            )
            self.positions[position_index]["mark"] = round(
                self.positions[position_index]["mark"] * change_factor,
                2,
            )
        for option_list in [
            self.options_calls,
            self.options_puts,
        ]:
            for option in option_list:
                change_factor = random.uniform(0.98, 1.02)
                option["mark"] = round(option["mark"] * change_factor, 2)
                option["bid"] = round(option["bid"] * change_factor, 2)
                option["ask"] = round(option["ask"] * change_factor * 1.01, 2)
                option["delta"] = round(
                    option["delta"] * random.uniform(0.95, 1.05),
                    4,
                )
                option["iv"] = round(
                    option["iv"] * random.uniform(0.97, 1.03),
                    2,
                )

    @rx.event
    def set_active_main_tab(self, tab_name: str):
        self.active_main_tab = tab_name

    @rx.event
    def set_active_sub_tab(self, tab_name: str):
        self.active_sub_tab = tab_name

    @rx.event(background=True)
    async def start_simulation(self):
        """Starts the data simulation loop."""
        async with self:
            if self.running_simulation:
                return
            self.running_simulation = True
            self._generate_initial_chart_data()
        while True:
            async with self:
                if not self.running_simulation:
                    break
                self._update_data_simulation()
            yield
            if not self.running_simulation:
                break
            await asyncio.sleep(2)

    @rx.event
    def stop_simulation(self):
        """Stops the data simulation loop."""
        self.running_simulation = False
