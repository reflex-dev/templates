import reflex as rx

config = rx.Config(
    app_name="account_management_dashboard",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV3Plugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="light",
                has_background=False,
                radius="medium",
                accent_color="indigo",
            )
        ),
    ],
)
