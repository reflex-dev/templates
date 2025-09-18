import reflex as rx

config = rx.Config(
    app_name="chat_app",
    plugins=[rx.plugins.SitemapPlugin(), rx.plugins.TailwindV3Plugin()],
)
