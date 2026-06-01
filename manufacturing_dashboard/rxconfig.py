import reflex as rx

config = rx.Config(
    app_name="manufacturing_dashboard",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV3Plugin(),
        rx.plugins.RadixThemesPlugin(theme=rx.theme(appearance="light")),
    ],
)
