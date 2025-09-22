import reflex as rx

config = rx.Config(
    app_name="space_dashboard",
    plugins=[rx.plugins.SitemapPlugin(), rx.plugins.TailwindV3Plugin()],
)
