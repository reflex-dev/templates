import os

import reflex as rx

database_url = os.getenv("DATABASE_URL", "sqlite:///reflex.db")

config = rx.Config(
    app_name="customer_data",
    db_url=database_url,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="dark",
                has_background=True,
                radius="large",
                accent_color="grass",
            )
        ),
    ],
)
