"""Configuration for the enterprise demos."""

import reflex_enterprise as rxe

config = rxe.Config(
    app_name="enterprise",
    async_db_url="sqlite+aiosqlite:///reflex.db",
    use_single_port=True,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    stylesheets=["xy-theme.css", "style.css"],
)
