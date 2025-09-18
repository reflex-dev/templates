import reflex as rx

config = rx.Config(
    app_name="admin_panel",
    plugins=[rx.plugins.SitemapPlugin(), rx.plugins.TailwindV3Plugin()],
)
