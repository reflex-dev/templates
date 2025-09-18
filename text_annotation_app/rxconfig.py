import reflex as rx

config = rx.Config(
    app_name="text_annotation_app",
    plugins=[rx.plugins.SitemapPlugin(), rx.plugins.TailwindV3Plugin()],
)
