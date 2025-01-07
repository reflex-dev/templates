import reflex as rx

from ..backend.backend import State
from ..components.stats_selector import stats_selector


class StatsState(rx.State):
    stats_view: str = "age_salary"
    radar_toggle: bool = False
    area_toggle: bool = False

    def toggle_radarchart(self):
        self.radar_toggle = not self.radar_toggle

    def toggle_areachart(self):
        self.area_toggle = not self.area_toggle


def _age_salary_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(cursor=False),
            rx.recharts.cartesian_grid(),
            rx.recharts.area(
                type_="monotone",
                data_key="average salary",
                stroke="#30A46C",
                fill="#5bb98bb3",
            ),
            rx.recharts.x_axis(data_key="age"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_age_salary_chart_data,
            min_height=325,
        ),
        rx.recharts.bar_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(),
            rx.recharts.bar(
                data_key="average salary", stroke="#30A46C", fill="#5bb98bb3"
            ),
            rx.recharts.x_axis(data_key="age"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_age_salary_chart_data,
            min_height=325,
        ),
    )


def _position_salary_chart() -> rx.Component:
    return rx.cond(
        StatsState.radar_toggle,
        rx.recharts.radar_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(cursor=False),
            rx.recharts.radar(
                data_key="average salary",
                stroke="#0090FF",
                fill="#0091ffa1",
            ),
            rx.recharts.polar_grid(),
            rx.recharts.polar_angle_axis(data_key="position"),
            data=State.get_position_salary_chart_data,
            min_height=325,
        ),
        rx.recharts.bar_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(),
            rx.recharts.bar(
                data_key="average salary", stroke="#0090FF", fill="#0091ffa1"
            ),
            rx.recharts.x_axis(data_key="position"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_position_salary_chart_data,
            min_height=325,
        ),
    )


def _team_salary_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(cursor=False),
            rx.recharts.cartesian_grid(),
            rx.recharts.area(
                type_="monotone",
                data_key="average salary",
                stroke="#8E4EC6",
                fill="#8e4ec6a9",
            ),
            rx.recharts.brush(data_key="name", height=30, stroke="#8E4EC6"),
            rx.recharts.x_axis(data_key="team"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_team_salary_chart_data,
            min_height=325,
        ),
        rx.recharts.bar_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(cursor=False),
            rx.recharts.cartesian_grid(),
            rx.recharts.bar(
                data_key="average salary",
                stroke="#8E4EC6",
                fill="#8e4ec6a9",
            ),
            rx.recharts.brush(data_key="name", height=30, stroke="#8E4EC6"),
            rx.recharts.x_axis(data_key="team"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_team_salary_chart_data,
            min_height=325,
        ),
    )


def _college_salary_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(cursor=False),
            rx.recharts.cartesian_grid(),
            rx.recharts.area(
                type_="monotone",
                data_key="average salary",
                stroke="#fdc313",
                fill="#ffc720a3",
            ),
            rx.recharts.brush(data_key="name", height=30, stroke="#fdc313"),
            rx.recharts.x_axis(data_key="college"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_college_salary_chart_data,
            min_height=325,
        ),
        rx.recharts.bar_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(),
            rx.recharts.bar(
                data_key="average salary", stroke="#fdc313", fill="#ffc720a3"
            ),
            rx.recharts.brush(data_key="name", height=30, stroke="#fdc313"),
            rx.recharts.x_axis(data_key="college"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_college_salary_chart_data,
            min_height=325,
        ),
    )


def _age_team_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(cursor=False),
            rx.recharts.cartesian_grid(),
            rx.recharts.area(
                data_key="average age",
                type_="monotone",
                stroke="#FFA500",
                fill="#ffa6009e",
            ),
            rx.recharts.brush(data_key="team", height=30, stroke="#FFA500"),
            rx.recharts.x_axis(data_key="team"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_team_age_average_data,
            min_height=325,
        ),
        rx.recharts.bar_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(),
            rx.recharts.bar(data_key="average age", stroke="#FFA500", fill="#ffa6009e"),
            rx.recharts.brush(data_key="team", height=30, stroke="#FFA500"),
            rx.recharts.x_axis(data_key="team"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_team_age_average_data,
            min_height=325,
        ),
    )


def _age_position_chart() -> rx.Component:
    return rx.cond(
        StatsState.radar_toggle,
        rx.recharts.radar_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(),
            rx.recharts.radar(
                data_key="average age",
                stroke="#E54666",
                fill="#e54666a0",
            ),
            rx.recharts.polar_grid(),
            rx.recharts.polar_angle_axis(data_key="position"),
            data=State.get_position_age_average_data,
            min_height=325,
        ),
        rx.recharts.bar_chart(
            rx.recharts.legend(),
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(),
            rx.recharts.bar(data_key="average age", stroke="#E54666", fill="#e54666a0"),
            rx.recharts.brush(data_key="position", height=30, stroke="#E54666"),
            rx.recharts.x_axis(data_key="position"),
            rx.recharts.y_axis(type_="number", scale="auto", hide=True),
            data=State.get_position_age_average_data,
            min_height=325,
        ),
    )


def _radar_toggle() -> rx.Component:
    return rx.cond(
        StatsState.radar_toggle,
        rx.icon_button(
            rx.icon("pentagon", size=24),
            size="3",
            cursor="pointer",
            variant="soft",
            on_click=StatsState.toggle_radarchart,
        ),
        rx.icon_button(
            rx.icon("bar-chart-3", size=24),
            size="3",
            cursor="pointer",
            variant="soft",
            on_click=StatsState.toggle_radarchart,
        ),
    )


def _area_toggle() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.icon_button(
            rx.icon("area-chart", size=24),
            size="3",
            cursor="pointer",
            variant="soft",
            on_click=StatsState.toggle_areachart,
        ),
        rx.icon_button(
            rx.icon("bar-chart-3", size=24),
            size="3",
            cursor="pointer",
            variant="soft",
            on_click=StatsState.toggle_areachart,
        ),
    )


def stats_ui() -> rx.Component:
    return rx.flex(
        rx.scroll_area(
            stats_selector(),
            scrollbars="vertical",
            width=["100%", "100%", "100%", "45%"],
            height=["100%", "100%", "100%", "calc(100vh - 300px)"],
            type="always",
        ),
        rx.vstack(
            rx.flex(
                rx.select(
                    value=StatsState.stats_view,
                    items=[
                        "age_salary",
                        "age_team",
                        "age_position",
                        "position_salary",
                        "team_salary",
                        "college_salary",
                    ],
                    on_change=StatsState.set_stats_view,
                    size="3",
                    variant="soft",
                    justify_content="end",
                ),
                rx.match(
                    StatsState.stats_view,
                    ("position_salary", "age_position", _radar_toggle()),
                    (_area_toggle()),
                ),
                margin_bottom=["2em", "2em", "4em"],
                spacing="4",
                width="100%",
            ),
            rx.match(
                StatsState.stats_view,
                ("age_salary", _age_salary_chart()),
                ("age_team", _age_team_chart()),
                ("age_position", _age_position_chart()),
                ("position_salary", _position_salary_chart()),
                ("team_salary", _team_salary_chart()),
                ("college_salary", _college_salary_chart()),
            ),
            width="100%",
            justify="center",
            padding_x=["0em", "0em", "0em", "0em", "6em"],
        ),
        flex_direction=["column-reverse", "column-reverse", "column-reverse", "row"],
        spacing="9",
        width="100%",
    )
