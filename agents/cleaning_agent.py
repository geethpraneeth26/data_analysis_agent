"""
Data Cleaning Agent
Performs comprehensive data cleaning on the raw DataFrame.
"""
import re
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer


class CleaningAgent:
    """Cleans and prepares the dataset for analysis."""

    name = "CleaningAgent"

    def run(self, state: dict) -> dict:
        state["agent_log"] = state.get("agent_log", [])
        df: pd.DataFrame = state.get("raw_df")
        col_types: dict = state.get("col_types", {})

        if df is None or df.empty:
            state["error"] = "CleaningAgent: No data to clean."
            return state

        df = df.copy()
        report = []

        # 1. Standardise column names
        original_cols = df.columns.tolist()
        df.columns = [self._standardise_col(c) for c in df.columns]
        renamed = [(o, n) for o, n in zip(original_cols, df.columns.tolist()) if o != n]
        if renamed:
            report.append(f"📝 Renamed {len(renamed)} column(s) to snake_case.")
            # Update col_types keys
            col_map = {self._standardise_col(o): self._standardise_col(o) for o in original_cols}
            col_types = self._remap_col_types(col_types, original_cols, df.columns.tolist())

        # 2. Strip whitespace from string columns
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"nan": np.nan, "None": np.nan, "": np.nan, "N/A": np.nan, "n/a": np.nan})
        report.append("📝 Stripped whitespace and standardised null placeholders in text columns.")

        # 3. Fix data types for numeric columns
        for col in col_types.get("numeric", []):
            col = self._standardise_col(col)
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # 4. Fix datetime columns
        for col in col_types.get("datetime", []):
            col = self._standardise_col(col)
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")

        # 5. Handle missing values
        missing_before = df.isnull().sum().sum()
        if missing_before > 0:
            numeric_cols_present = [c for c in col_types.get("numeric", []) if self._standardise_col(c) in df.columns]
            numeric_cols_present = [self._standardise_col(c) for c in numeric_cols_present]
            cat_cols_present = [c for c in col_types.get("categorical", []) if self._standardise_col(c) in df.columns]
            cat_cols_present = [self._standardise_col(c) for c in cat_cols_present]

            if numeric_cols_present:
                imputer = SimpleImputer(strategy="median")
                df[numeric_cols_present] = imputer.fit_transform(df[numeric_cols_present])

            if cat_cols_present:
                cat_imputer = SimpleImputer(strategy="most_frequent")
                df[cat_cols_present] = cat_imputer.fit_transform(df[cat_cols_present])

            missing_after = df.isnull().sum().sum()
            filled = missing_before - missing_after
            report.append(
                f"📝 Imputed {filled} missing value(s) "
                f"(numeric → median, categorical → mode). {missing_after} remain."
            )
        else:
            report.append("📝 No missing values detected.")

        # 6. Remove duplicates
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            df = df.drop_duplicates()
            report.append(f"📝 Removed {dup_count} duplicate row(s).")
        else:
            report.append("📝 No duplicate rows detected.")

        state["clean_df"] = df
        state["col_types"] = col_types
        state["cleaning_report"] = report
        state["agent_log"].append(
            f"✅ CleaningAgent: Cleaning complete. {len(report)} actions performed. "
            f"Final shape: {df.shape[0]} rows × {df.shape[1]} columns."
        )
        return state

    # ------------------------------------------------------------------

    def _standardise_col(self, name: str) -> str:
        name = str(name).strip()
        name = re.sub(r"[^\w\s]", "", name)
        name = re.sub(r"\s+", "_", name)
        name = name.lower()
        return name

    def _remap_col_types(self, col_types: dict, old_cols: list, new_cols: list) -> dict:
        mapping = {o: n for o, n in zip(old_cols, new_cols)}
        remapped = {}
        for kind, cols in col_types.items():
            remapped[kind] = [mapping.get(c, c) for c in cols]
        return remapped
