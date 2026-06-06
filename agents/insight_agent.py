"""
Insight Generation Agent
Converts analysis results into plain-language bullet-point insights.
"""
import pandas as pd
import numpy as np


class InsightAgent:
    """Generates natural language insights from analysis results."""

    name = "InsightAgent"

    def run(self, state: dict) -> dict:
        state["agent_log"] = state.get("agent_log", [])
        df: pd.DataFrame = state.get("clean_df")
        stats: dict = state.get("stats", {})
        trends: dict = state.get("trends", {})
        category_counts: dict = state.get("category_counts", {})
        correlations = state.get("correlations")
        numeric_cols: list = state.get("numeric_cols", [])
        cat_cols: list = state.get("cat_cols", [])

        insights = []

        if df is None or df.empty:
            state["insights"] = ["No data available for insight generation."]
            return state

        # Dataset size
        insights.append(
            f"📊 The dataset contains **{df.shape[0]:,} records** across **{df.shape[1]} attributes**."
        )

        # Numeric column insights
        for col, s in stats.items():
            col_label = col.replace("_", " ").title()
            mean_val = s.get("mean", 0)
            max_val = s.get("max", 0)
            min_val = s.get("min", 0)
            total = s.get("total", 0)
            std = s.get("std", 0)

            insights.append(
                f"🔢 **{col_label}**: Total = **{self._fmt(total)}**, "
                f"Average = **{self._fmt(mean_val)}**, "
                f"Range = {self._fmt(min_val)} → {self._fmt(max_val)}"
            )

            # High spread
            if mean_val != 0 and std / abs(mean_val) > 0.5:
                insights.append(
                    f"⚠️ **{col_label}** shows high variability (std = {self._fmt(std)}), "
                    "suggesting diverse values across records."
                )

            # Skew
            try:
                skew = df[col].skew()
                if abs(skew) > 1:
                    direction = "positively" if skew > 0 else "negatively"
                    insights.append(
                        f"📈 **{col_label}** distribution is {direction} skewed (skew = {skew:.2f}), "
                        "indicating a long tail on one side."
                    )
            except Exception:
                pass

        # Category insights
        for col, counts in category_counts.items():
            if not counts:
                continue
            col_label = col.replace("_", " ").title()
            top_cat = max(counts, key=counts.get)
            top_val = counts[top_cat]
            total_cat = sum(counts.values())
            pct = top_val / total_cat * 100 if total_cat else 0
            insights.append(
                f"🏆 **{col_label}**: Top category is **'{top_cat}'** "
                f"with {top_val:,} occurrences ({pct:.1f}% of records)."
            )
            if len(counts) > 1:
                second_cat = list(counts.keys())[1]
                second_val = list(counts.values())[1]
                diff = top_val - second_val
                insights.append(
                    f"   → **'{top_cat}'** leads **'{second_cat}'** by {diff:,} records."
                )

        # Trend insights
        for col, trend_df in trends.items():
            col_label = col.replace("_", " ").title()
            if trend_df is not None and len(trend_df) >= 2:
                first_val = trend_df.iloc[0, 1]
                last_val = trend_df.iloc[-1, 1]
                peak_idx = trend_df.iloc[:, 1].idxmax()
                peak_period = trend_df.iloc[peak_idx, 0]
                peak_val = trend_df.iloc[peak_idx, 1]

                change_pct = (last_val - first_val) / abs(first_val) * 100 if first_val != 0 else 0
                direction = "📈 grew" if change_pct >= 0 else "📉 declined"
                insights.append(
                    f"📅 **{col_label}** {direction} by **{abs(change_pct):.1f}%** over the observed period."
                )
                insights.append(
                    f"   → Peak period: **{str(peak_period)[:10]}** with {self._fmt(peak_val)}."
                )

        # Correlation insights
        if correlations is not None and not correlations.empty:
            corr_pairs = []
            cols = correlations.columns.tolist()
            for i in range(len(cols)):
                for j in range(i + 1, len(cols)):
                    val = correlations.iloc[i, j]
                    if not np.isnan(val) and abs(val) > 0.5:
                        corr_pairs.append((cols[i], cols[j], val))
            corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)

            for c1, c2, val in corr_pairs[:3]:
                kind = "strong positive" if val > 0 else "strong negative"
                insights.append(
                    f"🔗 **{c1.replace('_',' ').title()}** and "
                    f"**{c2.replace('_',' ').title()}** show a {kind} correlation "
                    f"(r = {val:.2f})."
                )

        state["insights"] = insights
        state["agent_log"].append(
            f"✅ InsightAgent: Generated {len(insights)} insights."
        )
        return state

    def _fmt(self, val) -> str:
        """Format a number nicely."""
        try:
            if float(val) == int(float(val)) and abs(float(val)) < 1e9:
                return f"{int(float(val)):,}"
            return f"{float(val):,.2f}"
        except Exception:
            return str(val)
