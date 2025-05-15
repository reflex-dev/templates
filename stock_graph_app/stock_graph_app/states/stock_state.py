from typing import List, TypedDict

import reflex as rx
import yfinance as yf


class HistoricalDataPoint(TypedDict):
    name: str
    price: float


def format_market_cap(cap):
    if cap is None:
        return "N/A"
    if cap >= 1_000_000_000_000:
        return f"{cap / 1_000_000_000_000:.2f}T"
    if cap >= 1_000_000_000:
        return f"{cap / 1_000_000_000:.2f}B"
    if cap >= 1_000_000:
        return f"{cap / 1_000_000:.2f}M"
    return str(cap)


class StockState(rx.State):
    """A state to fetch and display stock data."""

    search_ticker_input: str = "AAPL"
    company_info: dict = {}
    historical_data: List[HistoricalDataPoint] = []

    is_loading: bool = False
    error_message: str = ""

    selected_time_range: str = "1Y"
    time_ranges: list[str] = ["1D", "5D", "1M", "6M", "1Y", "5Y", "MAX"]

    _PERIOD_INTERVAL_MAP = {
        "1D": {"period": "1d", "interval": "5m"},
        "5D": {"period": "5d", "interval": "30m"},
        "1M": {"period": "1mo", "interval": "1d"},
        "6M": {"period": "6mo", "interval": "1d"},
        "1Y": {"period": "1y", "interval": "1d"},
        "5Y": {"period": "5y", "interval": "1wk"},
        "MAX": {"period": "max", "interval": "1mo"},
    }
    _DEFAULT_PERIOD_INTERVAL = {"period": "1y", "interval": "1d"}

    @rx.event
    async def on_load_fetch(self):
        """Fetch initial data when the page loads."""
        if not self.company_info:
            await self.fetch_stock_data()

    def _determine_period_interval(self, time_range: str) -> dict:
        """Determines yfinance period and interval from UI time_range."""
        return self._PERIOD_INTERVAL_MAP.get(time_range, self._DEFAULT_PERIOD_INTERVAL)

    async def _internal_fetch_stock_data(self, ticker_symbol_to_fetch: str):
        """Internal logic to fetch company data and historical prices."""
        self.is_loading = True
        self.error_message = ""

        if not ticker_symbol_to_fetch:
            self.error_message = "Ticker symbol cannot be empty."
            self.is_loading = False
            return

        try:
            ticker = yf.Ticker(ticker_symbol_to_fetch)

            if (
                not self.company_info
                or self.company_info.get("symbol") != ticker_symbol_to_fetch
            ):
                info = ticker.info
                if (
                    not info
                    or info.get("quoteType") == "NONE"
                    or info.get("longName") is None
                ):
                    self.error_message = f"Could not retrieve data for {ticker_symbol_to_fetch}. It might be an invalid ticker."
                    self.company_info = {}
                    self.historical_data = []
                    self.is_loading = False
                    return
                self.company_info = info
                self.search_ticker_input = ticker_symbol_to_fetch

            params = self._determine_period_interval(self.selected_time_range)
            hist_df = ticker.history(
                period=params["period"], interval=params["interval"]
            )

            if hist_df.empty:
                self.historical_data = []
                self.error_message = f"No historical data found for {ticker_symbol_to_fetch} for the selected range."
            else:
                hist_df = hist_df.reset_index()
                date_col_found = False
                if "Datetime" in hist_df.columns:
                    hist_df["name"] = hist_df["Datetime"].dt.strftime("%b %d %Y %H:%M")
                    date_col_found = True
                elif "Date" in hist_df.columns:
                    hist_df["name"] = hist_df["Date"].dt.strftime("%b %d %Y")
                    date_col_found = True

                if date_col_found:
                    hist_df["price"] = hist_df["Close"].round(2)
                    self.historical_data = hist_df[["name", "price"]].to_dict("records")
                else:
                    self.historical_data = []
                    self.error_message = (
                        "Date information missing from historical data."
                    )

        except Exception as e:
            self.error_message = (
                f"Error fetching data for {ticker_symbol_to_fetch}: {e!s}"
            )
            if self.company_info.get("symbol") == ticker_symbol_to_fetch:
                self.historical_data = []
        finally:
            self.is_loading = False

    @rx.event
    async def fetch_stock_data(self, form_data: dict | None = None):
        """Fetch company data and historical prices using yfinance, triggered by form."""
        ticker_to_use = self.search_ticker_input
        if form_data and "ticker_input" in form_data and form_data["ticker_input"]:
            ticker_to_use = form_data["ticker_input"].upper()
            self.search_ticker_input = ticker_to_use

        if not ticker_to_use:
            self.error_message = "Please enter a ticker symbol."
            self.is_loading = False
            return

        await self._internal_fetch_stock_data(ticker_to_use)

    @rx.event
    async def refresh_data(self):
        """Refreshes the data for the current search_ticker_input."""
        if self.search_ticker_input:
            await self._internal_fetch_stock_data(self.search_ticker_input)
        else:
            self.error_message = "No ticker symbol to refresh."

    @rx.event
    async def set_time_range(self, time_range: str):
        """Set the time range and refetch historical data."""
        self.selected_time_range = time_range
        if self.company_info and self.company_info.get("symbol"):
            await self.fetch_stock_data()

    @rx.var
    def logo_url(self) -> str:
        """Constructs the URL for the company logo."""
        ticker = self.stock_ticker
        if ticker and ticker != "N/A":
            return f"https://assets.parqet.com/logos/symbol/{ticker.upper()}"
        return ""

    @rx.var
    def stock_ticker(self) -> str:
        return self.company_info.get("symbol", "N/A")

    @rx.var
    def company_name(self) -> str:
        return self.company_info.get("longName", "Company Name")

    @rx.var
    def exchange_info(self) -> str:
        exchange = self.company_info.get("exchange", "N/A")
        currency = self.company_info.get("currency", "")
        display_parts = [exchange]
        if currency:
            display_parts.append(f"Currency: {currency.upper()}")
        return " · ".join(filter(None, display_parts))

    @rx.var
    def current_price_display_val(self) -> str:
        price = self.company_info.get("currentPrice") or self.company_info.get(
            "regularMarketPrice"
        )
        if price is not None:
            return f"{price:.2f}"
        return "N/A"

    @rx.var
    def market_cap_display_val(self) -> str:
        return format_market_cap(self.company_info.get("marketCap"))

    @rx.var
    def is_market_currently_active(self) -> bool:
        """Determines if the market is currently in an active trading session (regular, pre, or post)."""
        market_state = self.company_info.get("marketState", "").upper()
        # Active states include regular market, pre-market, and post-market trading
        active_states = ["REGULAR", "PRE", "POST", "POSTPOST"]
        return market_state in active_states

    @rx.var
    def _after_hours_data(self) -> tuple[float | None, float | None, str]:
        info = self.company_info
        market_state = info.get("marketState")

        if market_state == "PRE":
            price = info.get("preMarketPrice")
            change = info.get("preMarketChange")
            if price is not None and change is not None:
                return price, change, "Pre-Market"
        elif market_state in ["POST", "POSTPOST", "CLOSED"]:
            price = info.get("postMarketPrice")
            change = info.get("postMarketChange")
            if price is not None and change is not None:
                return price, change, "After Hours"

        return None, None, ""

    @rx.var
    def after_hours_price_display_val(self) -> str:
        price, _, _ = self._after_hours_data
        if price is not None:
            return f"{price:.2f}"
        return ""

    @rx.var
    def after_hours_change_display_val(self) -> str:
        _, change, _ = self._after_hours_data
        if change is not None:
            sign = "+" if change > 0 else ""
            return f"{sign}{change:.2f}"
        return ""

    @rx.var
    def after_hours_label(self) -> str:
        _, _, label = self._after_hours_data
        return label

    @rx.var
    def show_after_hours_section(self) -> bool:
        price, change, _ = self._after_hours_data
        return price is not None and change is not None

    @rx.var
    def currency_code(self) -> str:
        """Returns the upper-cased currency code, defaulting to USD."""
        return self.company_info.get("currency", "USD").upper()

    @rx.var
    def y_axis_label_config(self) -> dict:
        """Provides configuration for the Y-axis label (title)."""
        return {
            "value": self.currency_code,
            "angle": -90,
            "position": "insideLeft",
            "style": {"textAnchor": "middle", "fill": "#d4d4d4"},
            "dy": 70,
            "dx": -15,
        }

    @rx.var
    def current_stock_data_for_chart(self) -> List[HistoricalDataPoint]:
        if not self.historical_data:
            return [{"name": "N/A", "price": 0}]
        return self.historical_data

    @rx.var
    def y_axis_domain(self) -> list[float | str]:
        if not self.historical_data:
            return ["auto", "auto"]
        prices = [d["price"] for d in self.historical_data if d["price"] is not None]
        if not prices:
            return [0, 100]
        min_price = min(prices)
        max_price = max(prices)
        padding = (max_price - min_price) * 0.05
        return [round(max(0, min_price - padding)), round(max_price + padding)]

    @rx.var
    def has_data_to_display(self) -> bool:
        return bool(
            self.company_info
            and self.company_info.get("symbol")
            and self.historical_data
        )
