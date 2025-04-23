import reflex as rx

from manufacturing_dashboard.states.dashboard_state import (
    DashboardState,
    SpcDataPoint,
)


def render_ooc_dot(
    point: rx.Var[SpcDataPoint],
) -> rx.Component:
    """Renders a ReferenceDot for an out-of-control point."""
    return rx.recharts.reference_dot(
        x=point["name"],
        y=point["value"].to(str),
        r=5,
        fill="#ef4444",
        stroke="none",
        is_front=True,
        if_overflow="discard",
    )


def spc_chart() -> rx.Component:
    """Renders the Live SPC (Statistical Process Control) chart."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Live SPC Chart: Diameter",
                class_name="text-xl font-semibold text-slate-200",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(class_name="w-3 h-0.5 bg-amber-400 mr-1.5"),
                    rx.el.span(
                        "Measurement",
                        class_name="text-xs text-slate-400 mr-4",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.el.div(class_name="w-2.5 h-2.5 bg-red-500 rounded-full mr-1.5"),
                    rx.el.span(
                        "Out of Control",
                        class_name="text-xs text-slate-400 mr-4",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.recharts.responsive_container(
            rx.recharts.composed_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3",
                    stroke="#475569",
                    horizontal=True,
                    vertical=False,
                ),
                rx.recharts.y_axis(
                    domain=[
                        DashboardState.lcl - 0.005,
                        DashboardState.ucl + 0.005,
                    ],
                    allow_data_overflow=True,
                    type_="number",
                    width=60,
                    tick_line=False,
                    axis_line=False,
                    stroke="#94a3b8",
                    tick_formatter="(value) => value.toFixed(3)",
                    tick_margin=10,
                ),
                rx.recharts.x_axis(
                    data_key="name",
                    type_="number",
                    stroke="#64748b",
                    tick_line=False,
                    axis_line=False,
                    tick=False,
                    domain=["dataMin", "dataMax"],
                    height=10,
                ),
                rx.recharts.reference_area(
                    y1=DashboardState.lsl.to_string(),
                    y2=DashboardState.usl.to_string(),
                    stroke_opacity=0.3,
                    fill="#0d9488",
                    fill_opacity=0.1,
                    stroke="#0f766e",
                    label=rx.recharts.label(
                        value="Spec",
                        position="insideTopRight",
                        fill="#5eead4",
                        offset=10,
                        font_size="10px",
                    ),
                ),
                rx.recharts.reference_line(
                    y=DashboardState.target_mean.to_string(),
                    stroke="#f59e0b",
                    stroke_dasharray="5 5",
                    stroke_width=1,
                    label="Target",
                ),
                rx.recharts.line(
                    data_key="value",
                    stroke="#fbbf24",
                    stroke_width=2,
                    dot=False,
                    type_="monotone",
                    name="Diameter",
                    is_animation_active=False,
                ),
                rx.foreach(
                    DashboardState.ooc_points,
                    render_ooc_dot,
                ),
                data=DashboardState.spc_chart_data,
                margin={
                    "top": 10,
                    "right": 30,
                    "left": 10,
                    "bottom": 10,
                },
            ),
            height=350,
        ),
        class_name="bg-slate-800 p-6 rounded-lg shadow-lg border border-slate-700 w-full mb-6",
    )
