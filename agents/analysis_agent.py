"""
Data Analysis Agent
Performs statistical analysis on the cleaned DataFrame.
"""
import pandas as pd
import numpy as np


class AnalysisAgent:
    """Runs statistical analysis on the cleaned dataset."""

    name = "AnalysisAgent"

    def run(self, state: dict) -> dict:
        state["agent_log"] = state.get("agent_log", [])
        df: pd.DataFrame = state.get("clean_df")
        col_types: dict = state.get("col_types", {})

        if df is None or df.empty:
            state["error"] = "AnalysisAgent: No cleaned data to analyse."
            return state

        numeric_cols = [c for c in col_types.get("numeric", []) if c in df.columns]
        cat_cols = [c for c in col_types.get("categorical", []) if c in df.columns]
        dt_cols = [c for c in col_types.get("datetime", []) if c in df.columns]

        stats = {}
        trends = {}
        correlations = None
        category_counts = {}

        # Descriptive stats for numeric columns
        if numeric_cols:
            desc = df[numeric_cols].describe().T
            desc["total"] = df[numeric_cols].sum()
            stats = desc.to_dict(orient="index")

        # Category frequency
        for col in cat_cols:
            counts = df[col].value_counts().head(10)
            category_counts[col] = counts.to_dict()

        # Correlation matrix
        if len(numeric_cols) >= 2:
            correlations = df[numeric_cols].corr()

        # Trend analysis over time
        if dt_cols and numeric_cols:
            dt_col = dt_cols[0]
            df_sorted = df.sort_values(dt_col)
            for ncol in numeric_cols[:3]:
                try:
                    monthly = (
                        df_sorted.set_index(dt_col)[ncol]
                        .resample("ME")
                        .sum()
                        .reset_index()
                    )
                    monthly.columns = [dt_col, ncol]
                    trends[ncol] = monthly
                except Exception:
                    pass

        state["stats"] = stats
        state["trends"] = trends
        state["correlations"] = correlations
        state["category_counts"] = category_counts
        state["numeric_cols"] = numeric_cols
        state["cat_cols"] = cat_cols
        state["dt_cols"] = dt_cols

        state["agent_log"].append(
            f"✅ AnalysisAgent: Computed stats for {len(numeric_cols)} numeric, "
            f"{len(cat_cols)} categorical columns. "
            f"Trends detected: {len(trends)}."
        )
        return state
