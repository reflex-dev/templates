import reflex as rx

config = rx.Config(
    app_name="stock_market_dashboard",
    plugins=[rx.plugins.SitemapPlugin(), rx.plugins.TailwindV3Plugin()],
)
