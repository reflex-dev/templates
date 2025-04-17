import reflex as rx
from marketing_dashboard.states.marketing_dashboard_state import (
    MarketingDashboardState,
)
from marketing_dashboard.components.line_chart_card import line_chart_card
from marketing_dashboard.components.progress_card import progress_card
from marketing_dashboard.components.data_list_card import data_list_card
from marketing_dashboard.components.kpi_only_card import kpi_only_card
from marketing_dashboard.components.footer import footer


def index() -> rx.Component:
    """The main dashboard page."""
    return rx.el.div(
        rx.el.main(
            rx.el.div(
                line_chart_card(
                    title="Sessions",
                    data=MarketingDashboardState.sessions_chart_data,
                    y_max=6000,
                    kpi_value=MarketingDashboardState.sessions_total,
                    kpi_desc="past 7 days",
                ),
                line_chart_card(
                    title="Conversions",
                    data=MarketingDashboardState.conversions_chart_data,
                    y_max=150,
                    kpi_value=MarketingDashboardState.conversions_total,
                    kpi_desc="past 7 days",
                ),
                progress_card(
                    title="Google Ads",
                    budget_spent=MarketingDashboardState.google_ads_spent,
                    budget_total=MarketingDashboardState.google_ads_budget,
                    progress_value=MarketingDashboardState.google_ads_progress,
                    conversion_count=MarketingDashboardState.google_ads_conversions,
                    cost_per_conversion=MarketingDashboardState.google_ads_cpc,
                ),
                progress_card(
                    title="Facebook",
                    budget_spent=MarketingDashboardState.facebook_ads_spent,
                    budget_total=MarketingDashboardState.facebook_ads_budget,
                    progress_value=MarketingDashboardState.facebook_ads_progress,
                    conversion_count=MarketingDashboardState.facebook_ads_conversions,
                    cost_per_conversion=MarketingDashboardState.facebook_ads_cpc,
                    show_warning_conv=True,
                ),
                data_list_card(
                    title="Sessions by medium",
                    data=MarketingDashboardState.sessions_by_medium,
                    value_key="value",
                ),
                data_list_card(
                    title="Conversions by medium",
                    data=MarketingDashboardState.conversions_by_medium,
                    value_key="value",
                ),
                kpi_only_card(
                    primary_value=MarketingDashboardState.google_ads_sessions,
                    primary_desc="sessions",
                    secondary_value=MarketingDashboardState.google_ads_sessions_cpc,
                    secondary_desc="cpc",
                ),
                kpi_only_card(
                    primary_value=MarketingDashboardState.facebook_ads_sessions,
                    primary_desc="sessions",
                    secondary_value=MarketingDashboardState.facebook_ads_sessions_cpc,
                    secondary_desc="cpc",
                    show_warning=True,
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        footer(),
        class_name="min-h-screen bg-indigo-950 text-white font-sans",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)
