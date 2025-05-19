"""Databricks + Reflex Taxi Fare Prediction App.

Uses the `samples.nyctaxi` dataset from Databricks to calculate the average fare
between two zip codes.
"""

import functools
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Iterator, Literal

import databricks.sql
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import reflex as rx
import reflex_enterprise as rxe
from databricks.sdk.core import Config

if TYPE_CHECKING:
    from databricks.sql.client import Cursor
    from databricks.sql.parameters.native import TParameterCollection


databricks_cfg = Config()  # Pull environment variables for auth
databricks_http_path = f"/sql/1.0/warehouses/{databricks_cfg.warehouse_id}"


@contextmanager
def databricks_cursor() -> Iterator["Cursor"]:
    with (
        databricks.sql.connect(
            server_hostname=databricks_cfg.host,
            http_path=databricks_http_path,
            credentials_provider=lambda: databricks_cfg.authenticate,
        ) as connection,
        connection.cursor() as cursor,
    ):
        yield cursor


def sync_query_df(
    query: str,
    parameters: "TParameterCollection | None" = None,
) -> pd.DataFrame:
    with databricks_cursor() as cursor:
        cursor.execute(query, parameters=parameters)
        return cursor.fetchall_arrow().to_pandas()


async def async_query_df(
    query: str,
    parameters: "TParameterCollection | None" = None,
) -> pd.DataFrame:
    return await rx.run_in_thread(lambda: sync_query_df(query, parameters))


class DataState(rx.State):
    @rx.var(initial_value=pd.DataFrame(), interval=1800, backend=True)
    async def _data(self) -> pd.DataFrame:
        return await async_query_df("SELECT * FROM samples.nyctaxi.trips LIMIT 1000")

    @rx.var
    async def columns(self) -> list[dict[str, str]]:
        return [{"field": f} for f in (await self._data).columns]

    @rx.var
    async def data_records(self) -> list[dict]:
        return (await self._data).to_dict(orient="records")

    @rx.var
    async def scatter_figure(self) -> go.Figure:
        return px.scatter(
            await self._data,
            x="trip_distance",
            y="fare_amount",
        )


def fare_data_grid() -> rx.Component:
    return rxe.ag_grid(
        id="data-table",
        column_defs=DataState.columns,
        row_data=DataState.data_records,
        width="100%",
        height="30em",
    )


def fare_distribution_chart_recharts() -> rx.Component:
    return rx.recharts.scatter_chart(
        rx.recharts.scatter(data=DataState.data_records),
        rx.recharts.x_axis(data_key="trip_distance", type_="number"),
        rx.recharts.y_axis(data_key="fare_amount"),
        rx.recharts.tooltip(is_animation_active=False),
        width=700,
        height=300,
        style={
            "& .recharts-scatter-symbol": {
                "opacity": "0.5",
            },
        },
    )


def fare_distribution_chart_plotly() -> rx.Component:
    return rx.plotly(fig=DataState.scatter_figure)


class PredictionState(DataState):
    loading: rx.Field[bool] = rx.field(False)
    filters: rx.Field[dict[str, Any]] = rx.field(
        {
            "pickup_zip": 10103,
            "dropoff_zip": 10110,
        },
    )
    predicted_fare: rx.Field[float | None] = rx.field(None)

    def _calculate_predicted_fare(self, data: pd.DataFrame) -> float | None:
        """Calculate the predicted fare."""
        if self.filters.get("pickup_zip") and self.filters.get("dropoff_zip"):
            d = data[
                (data["pickup_zip"] == self.filters["pickup_zip"])
                & (data["dropoff_zip"] == self.filters["dropoff_zip"])
            ]
            return float(d["fare_amount"].mean()) if len(d) > 0 else None

    @rx.event
    async def update_prediction(self):
        self.loading = True
        yield
        try:
            self.predicted_fare = await rx.run_in_thread(
                functools.partial(
                    self._calculate_predicted_fare,
                    await self._data,
                )
            )
        finally:
            self.loading = False

    @rx.event
    async def update_prediction_zip(
        self,
        which_field: Literal["pickup_zip", "dropoff_zip"],
        value: str,
    ):
        self.filters[which_field] = int(value)
        yield PredictionState.update_prediction

    @rx.event
    async def random_valid_zips(self):
        """Generate a random valid zip codes."""
        random_row = (await self._data).sample(1).to_dict(orient="records")[0]
        self.filters["pickup_zip"] = random_row["pickup_zip"]
        self.filters["dropoff_zip"] = random_row["dropoff_zip"]


def fare_prediction_zip_input(
    which_field: Literal["pickup_zip", "dropoff_zip"],
) -> rx.Component:
    return rx.el.label(
        which_field,
        rx.input(
            value=PredictionState.filters[which_field],
            on_change=PredictionState.update_prediction_zip(which_field),
        ),
    )


def fare_prediction_form() -> rx.Component:
    return rx.form(
        rx.hstack(
            fare_prediction_zip_input("pickup_zip"),
            rx.vstack(
                rx.button("👉", variant="ghost", disabled=PredictionState.loading),
                rx.button(
                    "🎲",
                    variant="ghost",
                    on_click=PredictionState.random_valid_zips,
                ),
            ),
            fare_prediction_zip_input("dropoff_zip"),
            align="center",
        ),
        on_submit=PredictionState.update_prediction,
    )


def fare_prediction_widget() -> rx.Component:
    return rx.vstack(
        rx.heading("🚕 Predict Fare"),
        fare_prediction_form(),
        rx.spinner(
            rx.heading(
                rx.cond(
                    PredictionState.predicted_fare,
                    f"${PredictionState.predicted_fare:.2f}",
                    "♾️",
                ),
            ),
            loading=PredictionState.loading,
        ),
        align="center",
    )


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Taxi fare distribution", size="9"),
            rx.hstack(
                rx.card(fare_distribution_chart_recharts()),
                rx.card(fare_prediction_widget()),
                flex_wrap="wrap",
            ),
            fare_data_grid(),
        ),
        rx.logo(),
        size="4",
    )


app = rxe.App()
app.add_page(index)
