import reflex as rx
from typing import TypedDict, List, Literal, Union
import random
import datetime
import asyncio


class ChartDataPoint(TypedDict):
    time: str
    price: float


class Option(TypedDict):
    type: Literal["Call", "Put"]
    mark: float
    percent_change_to: float
    delta: float
    oi: int
    volume: int
    iv: float
    low: float
    high: float
    bid: float
    ask: float
    strike: float
    gamma: float


class Order(TypedDict):
    symbol: str
    status: Literal[
        "Sending", "Working", "Filled", "Canceled"
    ]
    side: Literal["Buy", "Sell"]
    type: Literal["Market", "Limit", "Stop market"]
    qty: int
    total_cost: float


class Position(TypedDict):
    symbol: str
    qty: float
    mkt_val: float
    day_return: float
    day_percent: float
    total_ret: float
    mark: float
    avg_cost: float
    bid: float
    ask: float
    delta: float
    gamma: float
    theta: float
    iv: Union[float, None]
    type: Literal["Equities", "Options"]
    dte: Union[int, str]


class StockInfo(TypedDict):
    symbol: str
    price: float
    change: float
    change_percent: float
    volume: str
    open: float
    high: float
    low: float
    close: float


class TradingState(rx.State):
    stock_info: StockInfo = {
        "symbol": "HMNI",
        "price": 182.92,
        "change": 3.65,
        "change_percent": 0.19,
        "volume": "268.38K",
        "open": 181.21,
        "high": 184.03,
        "low": 180.05,
        "close": 182.34,
    }
    chart_data: list[ChartDataPoint] = []
    options_calls: list[Option] = [
        {
            "type": "Call",
            "mark": 185.63,
            "percent_change_to": 8.73,
            "delta": 0.6837,
            "oi": 375,
            "volume": 1814,
            "iv": 8.73,
            "low": 174.32,
            "high": 185.43,
            "bid": 2.12,
            "ask": 2.59,
            "strike": 170.0,
            "gamma": 0.0,
        },
        {
            "type": "Call",
            "mark": 185.43,
            "percent_change_to": 2.35,
            "delta": 0.4321,
            "oi": 170,
            "volume": 412,
            "iv": 4.31,
            "low": 174.52,
            "high": 185.43,
            "bid": 1.02,
            "ask": 1.31,
            "strike": 175.0,
            "gamma": 0.0,
        },
        {
            "type": "Call",
            "mark": 185.43,
            "percent_change_to": 10.36,
            "delta": 0.4531,
            "oi": 321,
            "volume": 2310,
            "iv": 6.06,
            "low": 174.51,
            "high": 184.51,
            "bid": 0.78,
            "ask": 0.84,
            "strike": 180.0,
            "gamma": 0.0,
        },
        {
            "type": "Call",
            "mark": 185.43,
            "percent_change_to": 8.73,
            "delta": 0.6837,
            "oi": 151,
            "volume": 1896,
            "iv": 12.78,
            "low": 184.16,
            "high": 184.16,
            "bid": 0.07,
            "ask": 0.12,
            "strike": 185.0,
            "gamma": 0.0,
        },
        {
            "type": "Call",
            "mark": 185.28,
            "percent_change_to": 2.35,
            "delta": 0.4321,
            "oi": 337,
            "volume": 1896,
            "iv": 12.78,
            "low": 184.51,
            "high": 184.51,
            "bid": 0.03,
            "ask": 0.07,
            "strike": 190.0,
            "gamma": 0.0,
        },
        {
            "type": "Call",
            "mark": 185.1,
            "percent_change_to": 11.91,
            "delta": 0.7643,
            "oi": 170,
            "volume": 2310,
            "iv": 8.73,
            "low": 184.78,
            "high": 184.78,
            "bid": 0.01,
            "ask": 0.02,
            "strike": 195.0,
            "gamma": 0.0,
        },
    ]
    options_puts: list[Option] = [
        {
            "type": "Put",
            "mark": 185.63,
            "percent_change_to": 8.73,
            "delta": 0.6837,
            "oi": 375,
            "volume": 1814,
            "iv": 23.95,
            "low": 0.0,
            "high": 0.0,
            "bid": 0.01,
            "ask": 0.02,
            "strike": 170.0,
            "gamma": 515.81,
        },
        {
            "type": "Put",
            "mark": 185.63,
            "percent_change_to": 8.73,
            "delta": 0.4321,
            "oi": 170,
            "volume": 1696,
            "iv": 4.31,
            "low": 0.0,
            "high": 0.0,
            "bid": 0.03,
            "ask": 0.04,
            "strike": 175.0,
            "gamma": 532.09,
        },
        {
            "type": "Put",
            "mark": 185.63,
            "percent_change_to": 10.36,
            "delta": 0.4451,
            "oi": 321,
            "volume": 2310,
            "iv": 6.06,
            "low": 0.0,
            "high": 0.0,
            "bid": 0.48,
            "ask": 0.55,
            "strike": 180.0,
            "gamma": 505.21,
        },
        {
            "type": "Put",
            "mark": 185.63,
            "percent_change_to": 8.73,
            "delta": 0.3451,
            "oi": 151,
            "volume": 1896,
            "iv": 12.78,
            "low": 0.0,
            "high": 0.0,
            "bid": 0.87,
            "ask": 0.91,
            "strike": 185.0,
            "gamma": 515.81,
        },
        {
            "type": "Put",
            "mark": 185.28,
            "percent_change_to": 2.35,
            "delta": 0.6573,
            "oi": 337,
            "volume": 1896,
            "iv": 12.78,
            "low": 0.0,
            "high": 0.0,
            "bid": 1.06,
            "ask": 1.19,
            "strike": 190.0,
            "gamma": 505.21,
        },
        {
            "type": "Put",
            "mark": 185.1,
            "percent_change_to": 11.91,
            "delta": 0.462,
            "oi": 263,
            "volume": 1896,
            "iv": 12.78,
            "low": 0.0,
            "high": 0.0,
            "bid": 2.05,
            "ask": 2.32,
            "strike": 195.0,
            "gamma": 505.21,
        },
    ]
    recent_orders: list[Order] = [
        {
            "symbol": "STO",
            "status": "Sending",
            "side": "Buy",
            "type": "Market",
            "qty": 3,
            "total_cost": 970.14,
        },
        {
            "symbol": "LLAB",
            "status": "Working",
            "side": "Sell",
            "type": "Market",
            "qty": 5,
            "total_cost": 5319.02,
        },
        {
            "symbol": "HMNI",
            "status": "Filled",
            "side": "Buy",
            "type": "Market",
            "qty": 2,
            "total_cost": 368.76,
        },
        {
            "symbol": "SFFT Call Debit Spread",
            "status": "Filled",
            "side": "Sell",
            "type": "Limit",
            "qty": 2,
            "total_cost": 1970.19,
        },
        {
            "symbol": "EAIT",
            "status": "Canceled",
            "side": "Sell",
            "type": "Stop market",
            "qty": 1,
            "total_cost": 670.01,
        },
        {
            "symbol": "ICCI",
            "status": "Filled",
            "side": "Buy",
            "type": "Stop market",
            "qty": 20,
            "total_cost": 256.33,
        },
    ]
    positions: list[Position] = [
        {
            "symbol": "AAPM",
            "qty": 1.031,
            "mkt_val": 139.91,
            "day_return": 2.01,
            "day_percent": 0.06,
            "total_ret": 7.23,
            "mark": 204.85,
            "avg_cost": 204.85,
            "bid": 204.85,
            "ask": 204.85,
            "delta": 21.7785,
            "gamma": 0.0,
            "theta": 0.0,
            "iv": None,
            "type": "Equities",
            "dte": "--",
        },
        {
            "symbol": "SFFT",
            "qty": 11.43,
            "mkt_val": 5438.91,
            "day_return": -237.85,
            "day_percent": -7.21,
            "total_ret": 1970.14,
            "mark": 557.82,
            "avg_cost": 166.23,
            "bid": 162.1,
            "ask": 162.8,
            "delta": 10.0872,
            "gamma": 0.0,
            "theta": 0.0,
            "iv": None,
            "type": "Equities",
            "dte": "--",
        },
        {
            "symbol": "HMNI 10/17 $195 Call",
            "qty": 2,
            "mkt_val": 10439.91,
            "day_return": 532.68,
            "day_percent": 1.39,
            "total_ret": 3982.37,
            "mark": 832.19,
            "avg_cost": 198.02,
            "bid": 198.57,
            "ask": 199.03,
            "delta": -0.2307,
            "gamma": 0.0266,
            "theta": -0.4531,
            "iv": 25.5,
            "type": "Options",
            "dte": 4,
        },
        {
            "symbol": "HMNI",
            "qty": 2.04,
            "mkt_val": 10439.91,
            "day_return": 532.68,
            "day_percent": 1.39,
            "total_ret": 3982.37,
            "mark": 832.19,
            "avg_cost": 832.19,
            "bid": 832.19,
            "ask": 832.19,
            "delta": 4.035,
            "gamma": 0.0,
            "theta": 0.0,
            "iv": None,
            "type": "Equities",
            "dte": "--",
        },
        {
            "symbol": "LLAB",
            "qty": 2.04,
            "mkt_val": 439.91,
            "day_return": 12.01,
            "day_percent": 0.17,
            "total_ret": 24.98,
            "mark": 54.86,
            "avg_cost": 54.86,
            "bid": 54.86,
            "ask": 54.86,
            "delta": 49.9616,
            "gamma": 0.0,
            "theta": 0.0,
            "iv": None,
            "type": "Equities",
            "dte": "--",
        },
        {
            "symbol": "EEPO 10/19 $456 Put",
            "qty": 1,
            "mkt_val": 10439.91,
            "day_return": 1.01,
            "day_percent": 0.17,
            "total_ret": 832.19,
            "mark": 832.82,
            "avg_cost": 832.82,
            "bid": 832.02,
            "ask": 832.85,
            "delta": -0.4394,
            "gamma": 0.0186,
            "theta": -0.4394,
            "iv": 88.05,
            "type": "Options",
            "dte": 6,
        },
    ]
    active_main_tab: str = "Options trading"
    active_sub_tab: str = "4D Fri Oct 18"
    running_simulation: bool = False

    @rx.var
    def combined_options(
        self,
    ) -> List[dict[str, dict[str, int]]]:
        """Combine call and put options based on strike price."""
        calls_by_strike = {
            opt["strike"]: opt for opt in self.options_calls
        }
        puts_by_strike = {
            opt["strike"]: opt for opt in self.options_puts
        }
        all_strikes = sorted(
            list(
                set(calls_by_strike.keys())
                | set(puts_by_strike.keys())
            )
        )
        combined = []
        for strike in all_strikes:
            combined.append(
                {
                    "call": calls_by_strike.get(strike),
                    "put": puts_by_strike.get(strike),
                    "strike": strike,
                }
            )
        return combined

    def _generate_initial_chart_data(self):
        """Generates some initial random chart data."""
        if not self.chart_data:
            now = datetime.datetime.now(
                datetime.timezone.utc
            )
            start_price = self.stock_info["price"]
            data = []
            for i in range(60):
                time = now - datetime.timedelta(
                    minutes=59 - i
                )
                price_change = random.uniform(-0.5, 0.5)
                new_price = max(
                    0.1, start_price + price_change
                )
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
        new_price = round(
            max(0.1, old_price + price_change), 2
        )
        self.stock_info["price"] = new_price
        self.stock_info["change"] = round(
            new_price - self.stock_info["close"], 2
        )
        self.stock_info["change_percent"] = (
            round(
                self.stock_info["change"]
                / self.stock_info["close"]
                * 100,
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
            order_index = random.randint(
                0, len(self.recent_orders) - 1
            )
            statuses: List[
                Literal[
                    "Sending",
                    "Working",
                    "Filled",
                    "Canceled",
                ]
            ] = ["Sending", "Working", "Filled", "Canceled"]
            if (
                self.recent_orders[order_index]["status"]
                not in ["Filled", "Canceled"]
                or random.random() < 0.1
            ):
                self.recent_orders[order_index][
                    "status"
                ] = random.choice(statuses)
        if self.positions:
            position_index = random.randint(
                0, len(self.positions) - 1
            )
            change_factor = random.uniform(0.995, 1.005)
            old_mkt_val = self.positions[position_index][
                "mkt_val"
            ]
            new_mkt_val = round(
                old_mkt_val * change_factor, 2
            )
            self.positions[position_index][
                "mkt_val"
            ] = new_mkt_val
            day_return_change = (
                new_mkt_val - old_mkt_val
            ) * random.uniform(0.8, 1.2)
            self.positions[position_index]["day_return"] = (
                round(
                    self.positions[position_index][
                        "day_return"
                    ]
                    + day_return_change,
                    2,
                )
            )
            self.positions[position_index]["total_ret"] = (
                round(
                    self.positions[position_index][
                        "total_ret"
                    ]
                    + day_return_change,
                    2,
                )
            )
            self.positions[position_index]["mark"] = round(
                self.positions[position_index]["mark"]
                * change_factor,
                2,
            )
        for option_list in [
            self.options_calls,
            self.options_puts,
        ]:
            for option in option_list:
                change_factor = random.uniform(0.98, 1.02)
                option["mark"] = round(
                    option["mark"] * change_factor, 2
                )
                option["bid"] = round(
                    option["bid"] * change_factor, 2
                )
                option["ask"] = round(
                    option["ask"] * change_factor * 1.01, 2
                )
                option["delta"] = round(
                    option["delta"]
                    * random.uniform(0.95, 1.05),
                    4,
                )
                option["iv"] = round(
                    option["iv"]
                    * random.uniform(0.97, 1.03),
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