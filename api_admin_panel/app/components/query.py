import reflex as rx

from app.states.base import BaseState
from app.states.queries import QueryState, QueryAPI
from app.styles import text


def item_title(title: str):
    return (
        rx.hstack(
            rx.chakra.text(title, font_size="var(--chakra-fontSizes-md)", **text),
            rx.chakra.accordion_icon(),
            width="100%",
            justify_content="space-between",
        ),
    )


def item_add_event(event_trigger: callable):
    return rx.badge(
        rx.hstack(
            rx.text("+"),
            rx.text("add", weight="bold"),
            width="100%",
            justify_content="space-between",
        ),
        on_click=event_trigger,
        padding="0.35em 0.75em",
        cursor="pointer",
        color_scheme="gray",
    )


def form_item_entry(data: dict[str, str]):

    def create_entry(title: str, function: callable):
        return (
            rx.input(
                placeholder=title,
                width="100%",
                on_change=function,
                variant="surface",
            ),
        )

    return rx.hstack(
        create_entry("key", lambda key: QueryState.update_keyy(key, data)),
        create_entry("value", lambda value: QueryState.update_value(value, data)),
        rx.button(
            "DEL",
            on_click=QueryState.remove_entry(data),
            color_scheme="ruby",
            variant="surface",
            cursor="pointer",
        ),
        width="100%",
        spacing="1",
    )


def form_item(
    title: str, state: list[dict[str, str]], func: callable, event_trigger: callable
):
    return rx.chakra.accordion(
        rx.chakra.accordion_item(
            rx.chakra.accordion_button(item_title(title)),
            rx.chakra.accordion_panel(
                item_add_event(event_trigger),
                width="100%",
                display="flex",
                justify_content="end",
            ),
            rx.chakra.accordion_panel(
                rx.vstack(rx.foreach(state, func), width="100%", spacing="1")
            ),
        ),
        allow_toggle=True,
        width="100%",
    )


def form_body_param_item(
    state: list[dict[str, str]], func: callable, event_trigger: callable
):
    return rx.chakra.accordion(
        rx.chakra.accordion_item(
            rx.chakra.accordion_button(item_title("Body")),
            rx.chakra.accordion_panel(
                rx.match(
                    QueryState.current_req,
                    (
                        "GET",
                        rx.select(
                            QueryState.get_params_body,
                            default_value="None",
                            width="100%",
                        ),
                    ),
                    (
                        "POST",
                        rx.vstack(
                            rx.hstack(
                                item_add_event(event_trigger),
                                width="100%",
                                justify_content="end",
                            ),
                            rx.select(
                                QueryState.post_params_body,
                                default_value="JSON",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.foreach(state, func), width="100%", spacing="1"
                            ),
                            width="100%",
                        ),
                    ),
                ),
            ),
        ),
        allow_toggle=True,
        width="100%",
    )


def form_request_item():
    return rx.chakra.accordion(
        rx.chakra.accordion_item(
            rx.chakra.accordion_button(item_title("Requests")),
            rx.chakra.accordion_panel(
                rx.hstack(
                    rx.select(
                        QueryState.req_methods,
                        width="120px",
                        default_value="GET",
                        on_change=QueryState.get_request,
                    ),
                    rx.input(
                        value=QueryState.req_url,
                        width="100%",
                        on_change=QueryState.set_req_url,
                        placeholder="https://example_site.com/api/v2/endpoint.json",
                    ),
                    width="100%",
                )
            ),
        ),
        allow_toggle=True,
        width="100%",
    )


def render_query_form():
    return rx.vstack(
        form_request_item(),
        # form_item("URL Parameters"),
        form_item(
            "Headers", QueryState.headers, form_item_entry, QueryState.add_header
        ),
        form_body_param_item(QueryState.body, form_item_entry, QueryState.add_body),
        form_item(
            "Cookies", QueryState.cookies, form_item_entry, QueryState.add_cookies
        ),
        width="100%",
        spacing="0",
        padding="0.5em 0.75em",
    )


def render_query_header():
    return rx.hstack(
        rx.button("Run", size="2", on_click=QueryAPI.run_get_request),
        width="100%",
        border_bottom="1px solid rgba(41, 41, 41, 0.51)",
        padding="1em 1em",
        justify_content="end",
    )


def render_query_component():
    return rx.vstack(
        render_query_header(),
        render_query_form(),
        flex=["100%", "100%", "100%", "100%", "30%"],
        display=BaseState.query_component_toggle,
        box_shadow="0px 10px 20px 0px rgba(0, 0, 0, 0.31)",
        padding_bottom="0.75em",
        border_radius="10px",
        bg=rx.color_mode_cond(
            "faf9fb",
            "#1a181a",
        ),
    )
