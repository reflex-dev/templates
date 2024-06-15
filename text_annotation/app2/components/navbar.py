import reflex as rx


navbar: dict[str, str] = {
    "width": "100%",
    "padding": "1em 1.15em",
    "justify_content": "space-between",
    "bg": rx.color_mode_cond(
        "rgba(255, 255, 255, 0.81)",
        "rgba(18, 17, 19, 0.81)",
    ),
    "align_items": "center",
    "border_bottom": "1px solid rgba(46, 46, 46, 0.51)",
}

text: dict[str, str] = {
    "font_family": "var(--chakra-fonts-branding)",
    "font_weight": "var(--chakra-fontWeights-black)",
}


def render_navbar():
    return rx.hstack(
        rx.hstack(
            rx.box(
                rx.chakra.text(
                    "Text Classification App",
                    font_size="var(--chakra-fontSizes-lg)",
                    **text,
                ),
            ),
            display="flex",
            align_items="center",
        ),
        rx.hstack(
            rx.color_mode.switch(),
        ),
        **navbar,
    )
