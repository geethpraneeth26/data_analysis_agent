"""
Dataset Understanding Agent
Analyses the structure of the loaded DataFrame and generates a human-readable summary.
"""
import pandas as pd
import numpy as np


class UnderstandingAgent:
    """Understands the structure of the dataset."""

    name = "UnderstandingAgent"

    def run(self, state: dict) -> dict:
        state["agent_log"] = state.get("agent_log", [])
        df: pd.DataFrame = state.get("raw_df")

        if df is None or df.empty:
            state["error"] = "UnderstandingAgent: No data available to analyse."
            return state

        n_rows, n_cols = df.shape
        col_types = self._classify_columns(df)
        summary = self._build_summary(df, n_rows, n_cols, col_types)

        state["shape"] = (n_rows, n_cols)
        state["col_types"] = col_types
        state["dataset_summary"] = summary

        state["agent_log"].append(
            f"✅ UnderstandingAgent: {n_rows} rows, {n_cols} columns. "
            f"Numeric: {len(col_types['numeric'])}, "
            f"Categorical: {len(col_types['categorical'])}, "
            f"Datetime: {len(col_types['datetime'])}."
        )
        return state

    # ------------------------------------------------------------------

    def _classify_columns(self, df: pd.DataFrame) -> dict:
        numeric_cols = []
        categorical_cols = []
        datetime_cols = []

        for col in df.columns:
            series = df[col]

            # Try datetime
            if pd.api.types.is_datetime64_any_dtype(series):
                datetime_cols.append(col)
                continue

            # Try coercing to datetime
            if pd.api.types.is_object_dtype(series):
                try:
                    converted = pd.to_datetime(series, infer_datetime_format=True, errors="coerce")
                    if converted.notna().sum() / max(len(series), 1) > 0.7:
                        datetime_cols.append(col)
                        continue
                except Exception:
                    pass

            # Numeric
            if pd.api.types.is_numeric_dtype(series):
                numeric_cols.append(col)
            else:
                # Try coercing to numeric
                coerced = pd.to_numeric(series, errors="coerce")
                if coerced.notna().sum() / max(len(series), 1) > 0.7:
                    numeric_cols.append(col)
                else:
                    categorical_cols.append(col)

        return {
            "numeric": numeric_cols,
            "categorical": categorical_cols,
            "datetime": datetime_cols,
        }

    def _build_summary(self, df, n_rows, n_cols, col_types) -> str:
        lines = [
            f"**Dataset Shape:** {n_rows} rows × {n_cols} columns",
            f"**Column Names:** {', '.join(df.columns.tolist())}",
        ]
        if col_types["numeric"]:
            lines.append(f"**Numeric Columns ({len(col_types['numeric'])}):** {', '.join(col_types['numeric'])}")
        if col_types["categorical"]:
            lines.append(f"**Categorical Columns ({len(col_types['categorical'])}):** {', '.join(col_types['categorical'])}")
        if col_types["datetime"]:
            lines.append(f"**Date/Time Columns ({len(col_types['datetime'])}):** {', '.join(col_types['datetime'])}")

        missing = df.isnull().sum().sum()
        if missing > 0:
            lines.append(f"**Missing Values:** {missing} total ({missing / (n_rows * n_cols) * 100:.1f}% of all cells)")
        else:
            lines.append("**Missing Values:** None detected")

        dups = df.duplicated().sum()
        if dups > 0:
            lines.append(f"**Duplicate Rows:** {dups}")

        return "\n\n".join(lines)
