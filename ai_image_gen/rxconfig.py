import reflex as rx

config = rx.Config(
    app_name="ai_image_gen",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="inherit",
                has_background=True,
                scaling="100%",
                radius="none",
                accent_color="violet",
            )
        ),
    ],
)
