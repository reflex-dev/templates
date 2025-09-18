"""Pivot demo for AgGrid."""

import pandas as pd

import reflex_enterprise as rxe

from .common import demo

df = pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json")


@demo(
    route="/pivot",
    title="Pivot",
    description="AgGrid with pivoting",
)
def pivot_page():
    """¨Pivot demo."""
    return rxe.ag_grid(
        id="sandbox_grid",
        column_defs=[
            {"field": "country", "row_group": True},
            {"field": "sport", "pivot": True},
            {"field": "year", "pivot": True},
            {"field": "gold", "aggFunc": "sum"},
        ],
        loading=False,
        row_data=df.to_dict("records"),  # pyright: ignore [reportArgumentType]
        default_col_def={
            "flex": 1,
            "min_width": 130,
            "enable_value": True,
            "enable_row_group": True,
            "enable_pivot": True,
        },
        auto_group_column_def={
            "minWidth": 200,
            "pinned": "left",
        },
        pivot_mode=True,
        side_bar="columns",
        pivot_panel_show="always",
        width="100%",
        height="500px",
    )
