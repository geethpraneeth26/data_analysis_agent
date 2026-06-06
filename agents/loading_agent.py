"""
Loading Agent
Loads CSV, Excel, and JSON files into a pandas DataFrame and normalises it.
"""
import io
import pandas as pd
import numpy as np


class LoadingAgent:
    """Reads structured file formats into a standard DataFrame."""

    name = "LoadingAgent"

    def run(self, state: dict) -> dict:
        state["agent_log"] = state.get("agent_log", [])
        file_type = state.get("file_type")
        uploaded_file = state.get("uploaded_file")

        # If ExtractionAgent already produced a DataFrame, use it
        if state.get("extracted_df") is not None:
            state["raw_df"] = state["extracted_df"]
            state["agent_log"].append(
                "✅ LoadingAgent: Using DataFrame produced by ExtractionAgent."
            )
            return state

        try:
            uploaded_file.seek(0)

            if file_type == "csv":
                df = self._load_csv(uploaded_file)
            elif file_type == "excel":
                df = pd.read_excel(uploaded_file, engine="openpyxl")
            elif file_type == "json":
                df = self._load_json(uploaded_file)
            else:
                state["error"] = f"LoadingAgent: Cannot load file type '{file_type}' directly."
                return state

            state["raw_df"] = df
            state["agent_log"].append(
                f"✅ LoadingAgent: Loaded {df.shape[0]} rows × {df.shape[1]} columns."
            )
        except Exception as e:
            state["error"] = f"LoadingAgent failed: {e}"

        return state

    def _load_csv(self, file) -> pd.DataFrame:
        """Try multiple encodings and delimiters."""
        content = file.read()
        for enc in ["utf-8", "latin-1", "cp1252"]:
            try:
                text = content.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            text = content.decode("utf-8", errors="replace")

        from io import StringIO
        sample = text[:2000]
        delimiter = ","
        for d in [",", "\t", ";", "|"]:
            if sample.count(d) > sample.count(delimiter):
                delimiter = d

        return pd.read_csv(io.StringIO(text), sep=delimiter, engine="python")

    def _load_json(self, file) -> pd.DataFrame:
        content = file.read()
        import json
        data = json.loads(content)
        if isinstance(data, list):
            return pd.json_normalize(data)
        elif isinstance(data, dict):
            # Try to find the first list value
            for v in data.values():
                if isinstance(v, list):
                    return pd.json_normalize(v)
            return pd.json_normalize([data])
        return pd.DataFrame([data])
