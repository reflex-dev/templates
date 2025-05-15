import reflex as rx
import yfinance as yf


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
    historical_data: list[dict] = []

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
    def on_load_fetch(self):
        """Fetch initial data when the page loads."""
        if not self.company_info:  # Fetch only if no data yet
            yield StockState.fetch_stock_data()

    def _determine_period_interval(self, time_range: str) -> dict:
        """Determines yfinance period and interval from UI time_range."""
        return self._PERIOD_INTERVAL_MAP.get(time_range, self._DEFAULT_PERIOD_INTERVAL)

    @rx.event
    def fetch_stock_data(self, form_data: dict | None = None):
        """Fetch company data and historical prices using yfinance."""
        self.is_loading = True
        self.error_message = ""

        ticker_symbol_to_fetch = self.search_ticker_input
        if form_data and "ticker_input" in form_data and form_data["ticker_input"]:
            ticker_symbol_to_fetch = form_data["ticker_input"].upper()
            self.search_ticker_input = ticker_symbol_to_fetch

        if not ticker_symbol_to_fetch:
            self.error_message = "Please enter a ticker symbol."
            self.is_loading = False
            return

        try:
            ticker = yf.Ticker(ticker_symbol_to_fetch)

            if (
                not self.company_info
                or self.company_info.get("symbol") != ticker_symbol_to_fetch
            ):
                info = ticker.info  # Direct access to the info property
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

            params = self._determine_period_interval(self.selected_time_range)
            hist_df = ticker.history(
                period=params["period"], interval=params["interval"]
            )

            if hist_df.empty:
                self.historical_data = []
                self.error_message = f"No historical data found for {ticker_symbol_to_fetch} for the selected range."
            else:
                hist_df = hist_df.reset_index()
                if "Datetime" in hist_df.columns:
                    hist_df["name"] = hist_df["Datetime"].dt.strftime("%b %d %Y %H:%M")
                elif "Date" in hist_df.columns:
                    hist_df["name"] = hist_df["Date"].dt.strftime("%b %d %Y")
                else:
                    self.historical_data = []
                    self.is_loading = False
                    self.error_message = (
                        "Date information missing from historical data."
                    )
                    return

                hist_df["price"] = hist_df["Close"].round(2)
                self.historical_data = hist_df[["name", "price"]].to_dict("records")

            self.error_message = ""

        except Exception as e:
            self.error_message = (
                f"Error fetching data for {ticker_symbol_to_fetch}: {e!s}"
            )
        finally:
            self.is_loading = False

    def set_time_range(self, time_range: str):
        """Set the time range and refetch historical data."""
        self.selected_time_range = time_range
        if self.company_info and self.company_info.get("symbol"):
            self.fetch_stock_data()

    def set_search_ticker_input(self, value: str):
        self.search_ticker_input = value

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
    def after_hours_change_color(self) -> str:
        _, change, _ = self._after_hours_data
        if change is None:
            return "text-neutral-500"
        return (
            "text-green-500"
            if change > 0
            else "text-red-500"
            if change < 0
            else "text-neutral-500"
        )

    @rx.var
    def current_stock_data_for_chart(self) -> list[dict]:
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
