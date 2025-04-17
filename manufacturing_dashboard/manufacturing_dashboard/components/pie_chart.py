import reflex as rx

from manufacturing_dashboard.states.dashboard_state import DashboardState


def ooc_pie_chart() -> rx.Component:
    """Renders the Pie chart showing % OOC per Parameter."""
    return rx.el.div(
        rx.el.h2(
            "% OOC per Parameter",
            class_name="text-xl font-semibold text-slate-200 mb-4 text-center",
        ),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                rx.foreach(
                    DashboardState.pie_data,
                    lambda item, index: rx.recharts.cell(fill=item["fill"]),
                ),
                data=DashboardState.pie_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                outer_radius="80%",
                inner_radius="40%",
                padding_angle=2,
                label_line=False,
                label=False,
                is_animation_active=False,
            ),
            rx.recharts.legend(
                layout="vertical",
                vertical_align="middle",
                align="right",
                icon_size=10,
                icon_type="square",
                wrapper_style={
                    "fontSize": "12px",
                    "color": "#94a3b8",
                },
            ),
            margin={
                "top": 5,
                "right": 5,
                "left": 5,
                "bottom": 5,
            },
            height=320,
            width="100%",
        ),
        class_name="bg-slate-800 p-6 rounded-lg shadow-lg border border-slate-700 h-[380px] flex flex-col justify-between w-full",
    )
