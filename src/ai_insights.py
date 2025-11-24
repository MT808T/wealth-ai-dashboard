from __future__ import annotations

from typing import Literal

import pandas as pd
from openai import OpenAI


client = OpenAI()


def _language_name(lang_code: str) -> str:
    mapping = {
        "en": "English",
        "de": "German",
        "fr": "French",
        "it": "Italian",
        "es": "Spanish",
    }
    return mapping.get(lang_code, "English")


def generate_portfolio_insights(
    df: pd.DataFrame,
    lang_code: str = "en",
    focus: Literal["segment", "country"] = "segment",
) -> str:
    """
    Generate a short, management-style commentary on the filtered portfolio.
    The output is meant to support wealth management reporting, not give advice.
    """

    if df.empty:
        return "No clients match the current filters. Please broaden the selection."

    total_aum = float(df["aum_chf"].sum())
    avg_return = float(df["return_ytd"].mean())
    avg_vol = float(df["volatility"].mean())
    avg_sharpe = float(df["sharpe_ratio"].mean())

    by_segment = (
        df.groupby("segment")
        .agg(
            aum_chf=("aum_chf", "sum"),
            return_ytd=("return_ytd", "mean"),
            volatility=("volatility", "mean"),
        )
        .reset_index()
        .sort_values("aum_chf", ascending=False)
    )

    by_country = (
        df.groupby("country")
        .agg(
            aum_chf=("aum_chf", "sum"),
            return_ytd=("return_ytd", "mean"),
        )
        .reset_index()
        .sort_values("aum_chf", ascending=False)
    )

    context = {
        "total_aum_chf": round(total_aum, 2),
        "avg_return_ytd": round(avg_return, 4),
        "avg_volatility": round(avg_vol, 4),
        "avg_sharpe_ratio": round(avg_sharpe, 2),
        "segment_view": by_segment.to_dict(orient="records"),
        "country_view": by_country.to_dict(orient="records"),
        "n_clients": int(len(df)),
    }

    language = _language_name(lang_code)

    system_prompt = (
        "You are a wealth management reporting analyst. "
        "Given aggregated portfolio data, you write short, structured commentary "
        "for internal dashboards. You never give investment advice or recommendations. "
        "You only describe patterns in the data and possible operational follow-ups. "
        f"Write in {language}."
    )

    user_prompt = (
        "You are given portfolio summary data for a filtered client set in a private banking context.\n\n"
        f"DATA (JSON-like):\n{context}\n\n"
        "Write a concise narrative (max 10–12 sentences) with:\n"
        "1) A high-level overview of the filtered portfolio (size, return, risk).\n"
        "2) A comparison of client segments and which ones drive AUM and performance.\n"
        "3) A brief view by country (if relevant).\n"
        "4) Any notable patterns, concentrations, or outliers that might be worth a follow-up from RM or management.\n\n"
        "Keep the tone factual and neutral. Do not give investment advice. Do not speculate about the future."
    )

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.4,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return completion.choices[0].message.content.strip()
