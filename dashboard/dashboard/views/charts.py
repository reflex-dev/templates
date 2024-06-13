import reflex as rx
import random
import datetime


class StatsState(rx.State):
    area_toggle: bool = True
    timeframe: str = "Monthly"
    users_data = []
    revenue_data = []
    orders_data = []
    device_data = []
    yearly_device_data = []

    def toggle_areachart(self):
        self.area_toggle = not self.area_toggle

    def randomize_data(self):
        # If data is already populated, don't randomize
        if self.users_data:
            return

        for i in range(30, -1, -1):  # Include today's data
            self.revenue_data.append(
                {
                    "Date": (
                        datetime.datetime.now() - datetime.timedelta(days=i)
                    ).strftime("%m-%d"),
                    "Revenue": random.randint(1000, 5000),
                }
            )
        for i in range(30, -1, -1):
            self.orders_data.append(
                {
                    "Date": (
                        datetime.datetime.now() - datetime.timedelta(days=i)
                    ).strftime("%m-%d"),
                    "Orders": random.randint(100, 500),
                }
            )

        for i in range(30, -1, -1):
            self.users_data.append(
                {
                    "Date": (
                        datetime.datetime.now() - datetime.timedelta(days=i)
                    ).strftime("%m-%d"),
                    "Users": random.randint(100, 500),
                }
            )

        self.device_data = [
            {"name": "Desktop", "value": 23, "fill": "var(--blue-8)"},
            {"name": "Mobile", "value": 47, "fill": "var(--green-8)"},
            {"name": "Tablet", "value": 25, "fill": "var(--purple-8)"},
            {"name": "Other", "value": 5, "fill": "var(--red-8)"},
        ]

        self.yearly_device_data = [
            {"name": "Desktop", "value": 34, "fill": "var(--blue-8)"},
            {"name": "Mobile", "value": 46, "fill": "var(--green-8)"},
            {"name": "Tablet", "value": 21, "fill": "var(--purple-8)"},
            {"name": "Other", "value": 9, "fill": "var(--red-8)"},
        ]


def area_toggle() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.icon_button(
            rx.icon("area-chart"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=StatsState.toggle_areachart,
        ),
        rx.icon_button(
            rx.icon("bar-chart-3"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=StatsState.toggle_areachart,
        ),
    )


def users_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Users",
                stroke="var(--blue-9)",
                fill="var(--blue-7)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.users_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.graphing_tooltip(),
            rx.recharts.bar(
                data_key="Users",
                stroke="var(--blue-9)",
                fill="var(--blue-7)",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.users_data,
            height=425,
        ),
    )


def revenue_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Revenue",
                stroke="var(--green-9)",
                fill="var(--green-7)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.revenue_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.bar(
                data_key="Revenue",
                stroke="var(--green-9)",
                fill="var(--green-7)",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.revenue_data,
            height=425,
        ),
    )


def orders_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Orders",
                stroke="var(--purple-9)",
                fill="var(--purple-7)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.orders_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.bar(
                data_key="Orders",
                stroke="var(--purple-9)",
                fill="var(--purple-7)",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.orders_data,
            height=425,
        ),
    )


def pie_chart() -> rx.Component:
    return rx.cond(
        StatsState.timeframe == "Yearly",
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=StatsState.yearly_device_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                padding_angle=1,
                inner_radius="70",
                outer_radius="100",
                label=True,
            ),
            rx.recharts.legend(),
            height=300,
        ),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=StatsState.device_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                padding_angle=1,
                inner_radius="70",
                outer_radius="100",
                label=True,
            ),
            rx.recharts.legend(),
            height=300,
        ),
    )


def timeframe_select() -> rx.Component:
    return rx.select(
        ["Monthly", "Yearly"],
        default_value="Monthly",
        value=StatsState.timeframe,
        variant="surface",
        on_change=StatsState.set_timeframe,
    )
