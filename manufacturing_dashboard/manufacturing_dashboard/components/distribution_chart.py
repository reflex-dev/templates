import reflex as rx

from manufacturing_dashboard.states.dashboard_state import DashboardState


def distribution_chart() -> rx.Component:
    """Renders the vertical bar chart for distribution data."""
    return rx.el.div(
        rx.el.h2(
            "Diameter Distribution",
            class_name="text-xl font-semibold text-slate-200 mb-2 text-center px-4 pt-4",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                stroke="#475569",
                horizontal=True,
                vertical=False,
            ),
            rx.recharts.x_axis(data_key="name", type_="category", hide=True),
            rx.recharts.y_axis(
                type_="number",
                allow_decimals=False,
                axis_line=False,
                tick_line=False,
                width=30,
                stroke="#94a3b8",
                font_size="10px",
            ),
            rx.recharts.bar(
                data_key="value",
                fill="#fbbf24",
                radius=[4, 4, 0, 0],
                is_animation_active=False,
                label_list={
                    "position": "right",
                    "fill": "#e2e8f0",
                    "font_size": "10px",
                    "offset": 5,
                },
            ),
            data=DashboardState.distribution_data,
            layout="vertical",
            bar_category_gap="25%",
            margin={
                "top": 10,
                "right": 30,
                "left": 5,
                "bottom": 0,
            },
            width="100%",
            height=320,
        ),
        class_name="bg-slate-800 rounded-lg shadow-lg border border-slate-700 h-[380px] flex flex-col w-full",
    )
