"""
File Detection Agent
Determines the type of the uploaded file from its extension/MIME type.
"""
import os


SUPPORTED_TYPES = {
    ".csv": "csv",
    ".xlsx": "excel",
    ".xls": "excel",
    ".json": "json",
    ".pdf": "pdf",
    ".docx": "docx",
    ".doc": "docx",
    ".txt": "txt",
}


class FileDetectionAgent:
    """Detects what kind of file the user uploaded."""

    name = "FileDetectionAgent"

    def run(self, state: dict) -> dict:
        uploaded_file = state.get("uploaded_file")
        if uploaded_file is None:
            state["error"] = "No file uploaded."
            return state

        filename: str = uploaded_file.name
        ext = os.path.splitext(filename)[-1].lower()
        file_type = SUPPORTED_TYPES.get(ext)

        if file_type is None:
            state["error"] = (
                f"Unsupported file type '{ext}'. "
                f"Please upload one of: {', '.join(SUPPORTED_TYPES.keys())}"
            )
            return state

        state["file_type"] = file_type
        state["filename"] = filename
        state["agent_log"] = state.get("agent_log", [])
        state["agent_log"].append(
            f"✅ FileDetectionAgent: Detected file type **{file_type.upper()}** for '{filename}'"
        )
        return state
