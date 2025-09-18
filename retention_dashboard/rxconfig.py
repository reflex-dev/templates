import reflex as rx

config = rx.Config(
    app_name="retention_dashboard",
    plugins=[rx.plugins.SitemapPlugin(), rx.plugins.TailwindV3Plugin()],
)
