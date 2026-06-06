"""
Visualization Agent
Generates interactive Plotly charts based on user selections.
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


CHART_TYPES = ["Bar", "Line", "Pie", "Scatter", "Histogram", "Area", "Box", "Heatmap (Correlation)"]


class VisualizationAgent:
    """Generates Plotly charts from the cleaned dataset."""

    name = "VisualizationAgent"

    def run(self, state: dict) -> dict:
        """Pre-generate default charts and store them in state."""
        state["agent_log"] = state.get("agent_log", [])
        df: pd.DataFrame = state.get("clean_df")
        numeric_cols: list = state.get("numeric_cols", [])
        cat_cols: list = state.get("cat_cols", [])
        trends: dict = state.get("trends", {})
        correlations = state.get("correlations")

        auto_charts = []

        if df is None or df.empty:
            state["auto_charts"] = auto_charts
            return state

        # 1. Distribution of numeric columns (histogram)
        for col in numeric_cols[:2]:
            fig = self.make_histogram(df, col)
            auto_charts.append({"title": f"Distribution of {col.replace('_',' ').title()}", "fig": fig})

        # 2. Category frequency bar chart
        for col in cat_cols[:2]:
            counts = df[col].value_counts().head(10).reset_index()
            counts.columns = [col, "count"]
            fig = self.make_bar(counts, col, "count",
                                title=f"Top Categories in {col.replace('_',' ').title()}")
            auto_charts.append({"title": f"Category: {col.replace('_',' ').title()}", "fig": fig})

        # 3. Trend lines
        for col, trend_df in trends.items():
            if trend_df is not None and len(trend_df) >= 2:
                dt_col = trend_df.columns[0]
                fig = self.make_line(trend_df, dt_col, col,
                                     title=f"Trend: {col.replace('_',' ').title()} over Time")
                auto_charts.append({"title": f"Trend: {col.replace('_',' ').title()}", "fig": fig})

        # 4. Correlation heatmap
        if correlations is not None and not correlations.empty:
            fig = self.make_heatmap(correlations)
            auto_charts.append({"title": "Correlation Heatmap", "fig": fig})

        state["auto_charts"] = auto_charts
        state["agent_log"].append(
            f"✅ VisualizationAgent: Generated {len(auto_charts)} automatic chart(s)."
        )
        return state

    # ------------------------------------------------------------------
    # Chart factory methods (also called by UI for custom charts)
    # ------------------------------------------------------------------

    def make_bar(self, df, x_col, y_col, color_col=None, title="Bar Chart") -> go.Figure:
        fig = px.bar(
            df, x=x_col, y=y_col, color=color_col,
            title=title,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        return self._style(fig)

    def make_line(self, df, x_col, y_col, color_col=None, title="Line Chart") -> go.Figure:
        fig = px.line(
            df, x=x_col, y=y_col, color=color_col,
            title=title,
            template="plotly_dark",
            markers=True,
        )
        return self._style(fig)

    def make_pie(self, df, names_col, values_col, title="Pie Chart") -> go.Figure:
        fig = px.pie(
            df, names=names_col, values=values_col,
            title=title,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        return self._style(fig)

    def make_scatter(self, df, x_col, y_col, color_col=None, title="Scatter Chart") -> go.Figure:
        fig = px.scatter(
            df, x=x_col, y=y_col, color=color_col,
            title=title,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        return self._style(fig)

    def make_histogram(self, df, col, title=None) -> go.Figure:
        title = title or f"Distribution of {col}"
        fig = px.histogram(
            df, x=col,
            title=title,
            template="plotly_dark",
            nbins=30,
            color_discrete_sequence=["#7c3aed"],
        )
        return self._style(fig)

    def make_area(self, df, x_col, y_col, color_col=None, title="Area Chart") -> go.Figure:
        fig = px.area(
            df, x=x_col, y=y_col, color=color_col,
            title=title,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        return self._style(fig)

    def make_box(self, df, x_col, y_col=None, color_col=None, title="Box Plot") -> go.Figure:
        fig = px.box(
            df, x=x_col, y=y_col, color=color_col,
            title=title,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        return self._style(fig)

    def make_heatmap(self, corr_df: pd.DataFrame, title="Correlation Heatmap") -> go.Figure:
        fig = go.Figure(
            data=go.Heatmap(
                z=corr_df.values,
                x=corr_df.columns.tolist(),
                y=corr_df.columns.tolist(),
                colorscale="Viridis",
                zmin=-1, zmax=1,
                text=corr_df.round(2).values,
                texttemplate="%{text}",
            )
        )
        fig.update_layout(title=title, template="plotly_dark")
        return self._style(fig)

    def make_custom_chart(
        self, df, chart_type, x_col, y_col=None, color_col=None
    ) -> go.Figure:
        title = f"{chart_type}: {y_col or x_col} by {x_col}"
        ct = chart_type.lower()

        if ct == "bar":
            # Determine which columns to group by
            group_cols = [x_col]
            if color_col and color_col != x_col:
                group_cols.append(color_col)

            if y_col:
                # Aggregate by summing the value across the groups
                agg = df.groupby(group_cols)[y_col].sum().reset_index()
            else:
                # Aggregate by counting occurrences
                agg = df.groupby(group_cols).size().reset_index(name="count")
                y_col = "count"

            return self.make_bar(agg, x_col, y_col, color_col, title)
        elif ct == "line":
            return self.make_line(df, x_col, y_col, color_col, title)
        elif ct == "pie":
            counts = df[x_col].value_counts().head(15).reset_index()
            counts.columns = [x_col, "count"]
            return self.make_pie(counts, x_col, "count", title)
        elif ct == "scatter":
            return self.make_scatter(df, x_col, y_col, color_col, title)
        elif ct == "histogram":
            return self.make_histogram(df, x_col, title)
        elif ct == "area":
            return self.make_area(df, x_col, y_col, color_col, title)
        elif ct == "box":
            return self.make_box(df, x_col, y_col, color_col, title)
        elif "heatmap" in ct:
            numeric = df.select_dtypes(include="number")
            return self.make_heatmap(numeric.corr(), title="Correlation Heatmap")
        else:
            return self.make_histogram(df, x_col, title)

    def _style(self, fig: go.Figure) -> go.Figure:
        fig.update_layout(
            paper_bgcolor="rgba(15,15,30,0.0)",
            plot_bgcolor="rgba(15,15,30,0.0)",
            font=dict(family="Inter, sans-serif", color="#e2e8f0"),
            title_font=dict(size=16, color="#a78bfa"),
            legend=dict(bgcolor="rgba(0,0,0,0.3)"),
            margin=dict(l=40, r=20, t=50, b=40),
        )
        return fig
