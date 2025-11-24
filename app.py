from __future__ import annotations

import streamlit as st
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

from src.generate_data import generate_synthetic_portfolio
from src.ai_insights import generate_portfolio_insights



st.set_page_config(page_title="Wealth AI Dashboard", layout="wide")


LABELS = {
    "en": {
        "app_title": "Wealth AI Dashboard",
        "caption": "Synthetic portfolio analytics for a private banking context.",
        "filters_header": "Filters",
        "language_label": "Language",
        "segment_label": "Client segment",
        "country_label": "Country",
        "kpi_title": "Portfolio KPIs",
        "total_aum": "Total AUM (CHF)",
        "avg_return": "Average YTD return",
        "avg_sharpe": "Average Sharpe ratio",
        "n_clients": "Number of clients",
        "alloc_title": "Average asset allocation",
        "risk_return_title": "Risk / Return by client",
        "raw_data": "Raw data",
    },
    "de": {
        "app_title": "Wealth AI Dashboard",
        "caption": "Synthetische Portfolio-Analysen im Private-Banking-Kontext.",
        "filters_header": "Filter",
        "language_label": "Sprache",
        "segment_label": "Kundensegment",
        "country_label": "Land",
        "kpi_title": "Portfolio-Kennzahlen",
        "total_aum": "Gesamtes AUM (CHF)",
        "avg_return": "Durchschnittliche YTD-Rendite",
        "avg_sharpe": "Durchschnittliche Sharpe-Ratio",
        "n_clients": "Anzahl Kunden",
        "alloc_title": "Durchschnittliche Asset-Allokation",
        "risk_return_title": "Risiko/Rendite je Kunde",
        "raw_data": "Rohdaten",
    },
    "fr": {
        "app_title": "Wealth AI Dashboard",
        "caption": "Analytique de portefeuille synthétique pour la banque privée.",
        "filters_header": "Filtres",
        "language_label": "Langue",
        "segment_label": "Segment client",
        "country_label": "Pays",
        "kpi_title": "Indicateurs de portefeuille",
        "total_aum": "AUM total (CHF)",
        "avg_return": "Rendement YTD moyen",
        "avg_sharpe": "Ratio de Sharpe moyen",
        "n_clients": "Nombre de clients",
        "alloc_title": "Allocation d’actifs moyenne",
        "risk_return_title": "Risque / rendement par client",
        "raw_data": "Données brutes",
    },
    "it": {
        "app_title": "Wealth AI Dashboard",
        "caption": "Analisi di portafoglio sintetico in un contesto di private banking.",
        "filters_header": "Filtri",
        "language_label": "Lingua",
        "segment_label": "Segmento cliente",
        "country_label": "Paese",
        "kpi_title": "KPI di portafoglio",
        "total_aum": "AUM totale (CHF)",
        "avg_return": "Rendimento YTD medio",
        "avg_sharpe": "Sharpe ratio media",
        "n_clients": "Numero di clienti",
        "alloc_title": "Allocazione media degli asset",
        "risk_return_title": "Rischio / rendimento per cliente",
        "raw_data": "Dati grezzi",
    },
    "es": {
        "app_title": "Wealth AI Dashboard",
        "caption": "Analítica de cartera sintética en un contexto de banca privada.",
        "filters_header": "Filtros",
        "language_label": "Idioma",
        "segment_label": "Segmento de cliente",
        "country_label": "País",
        "kpi_title": "KPIs de la cartera",
        "total_aum": "AUM total (CHF)",
        "avg_return": "Rentabilidad YTD media",
        "avg_sharpe": "Ratio de Sharpe media",
        "n_clients": "Número de clientes",
        "alloc_title": "Asignación media de activos",
        "risk_return_title": "Riesgo / rentabilidad por cliente",
        "raw_data": "Datos en bruto",
    },
}


@st.cache_data
def load_data() -> pd.DataFrame:
    return generate_synthetic_portfolio(n_clients=1289, region="europe")


def render_kpis(df: pd.DataFrame, labels: dict[str, str]) -> None:
    total_aum = df["aum_chf"].sum()
    avg_return = df["return_ytd"].mean()
    avg_sharpe = df["sharpe_ratio"].mean()
    n_clients = len(df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(labels["total_aum"], f"{total_aum:,.0f}")
    c2.metric(labels["avg_return"], f"{avg_return * 100:.2f}%")
    c3.metric(labels["avg_sharpe"], f"{avg_sharpe:.2f}")
    c4.metric(labels["n_clients"], f"{n_clients}")

def render_client_distribution(df: pd.DataFrame, labels: dict[str, str]) -> None:
    st.subheader("Client distribution by segment")
    seg_counts = df["segment"].value_counts()
    st.bar_chart(seg_counts)


def render_allocation_chart(df: pd.DataFrame, labels: dict[str, str]) -> None:
    alloc = (
        df[["asset_equity", "asset_bonds", "asset_fx", "asset_alts"]]
        .mean()
        .rename(
            {
                "asset_equity": "Equity",
                "asset_bonds": "Bonds",
                "asset_fx": "FX",
                "asset_alts": "Alternatives",
            }
        )
    )
    st.subheader(labels["alloc_title"])
    st.bar_chart(alloc)


def render_risk_return(df: pd.DataFrame, labels: dict[str, str]) -> None:
    st.subheader(labels["risk_return_title"])
    st.scatter_chart(
        df,
        x="volatility",
        y="return_ytd",
        color="segment",
    )


def main() -> None:
    df = load_data()

    # ---- Sidebar: language + filters ----
    st.sidebar.header("Settings")

    lang_code = st.sidebar.selectbox(
        "Language",
        options=["en", "de", "fr", "it", "es"],
        format_func=lambda x: {
            "en": "English",
            "de": "Deutsch",
            "fr": "Français",
            "it": "Italiano",
            "es": "Español",
        }[x],
        index=0,  # default: English
    )
    labels = LABELS[lang_code]

    st.sidebar.header(labels["filters_header"])

    segments = ["All"] + sorted(df["segment"].unique())
    countries = ["All"] + sorted(df["country"].unique())

    sel_segment = st.sidebar.selectbox(labels["segment_label"], segments)
    sel_country = st.sidebar.selectbox(labels["country_label"], countries)

    filtered_df = df.copy()
    if sel_segment != "All":
        filtered_df = filtered_df[filtered_df["segment"] == sel_segment]
    if sel_country != "All":
        filtered_df = filtered_df[filtered_df["country"] == sel_country]

    # ---- Main layout ----
    st.title(labels["app_title"])
    st.caption(labels["caption"])

    st.markdown(f"### {labels['kpi_title']}")
    render_kpis(filtered_df, labels)

    render_client_distribution(filtered_df, labels)





    col1, col2 = st.columns(2)
    with col1:
        render_allocation_chart(filtered_df, labels)
    with col2:
        render_risk_return(filtered_df, labels)

    st.markdown("### AI portfolio insights")

    if st.button("Generate insights on filtered portfolio"):
        with st.spinner("Generating AI commentary on the current selection..."):
            insights = generate_portfolio_insights(filtered_df, lang_code=lang_code)
        st.markdown(insights)

    with st.expander(labels["raw_data"]):
        st.dataframe(filtered_df, use_container_width=True)


if __name__ == "__main__":
    main()
