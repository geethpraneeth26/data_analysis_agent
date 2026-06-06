"""
Manager Agent (Main Orchestrator)
Coordinates all specialized agents in the correct pipeline order.
"""
import traceback
from agents.file_detection_agent import FileDetectionAgent
from agents.extraction_agent import ExtractionAgent
from agents.loading_agent import LoadingAgent
from agents.understanding_agent import UnderstandingAgent
from agents.cleaning_agent import CleaningAgent
from agents.analysis_agent import AnalysisAgent
from agents.insight_agent import InsightAgent
from agents.visualization_agent import VisualizationAgent


class DataMindManager:
    """
    Orchestrates the full data analysis pipeline.

    Pipeline:
        FileDetection → [Extraction] → Loading → Understanding →
        Cleaning → Analysis → Insight → Visualization
    """

    def __init__(self):
        self.file_detection = FileDetectionAgent()
        self.extraction = ExtractionAgent()
        self.loading = LoadingAgent()
        self.understanding = UnderstandingAgent()
        self.cleaning = CleaningAgent()
        self.analysis = AnalysisAgent()
        self.insight = InsightAgent()
        self.visualization = VisualizationAgent()

    def execute_pipeline(self, uploaded_file, on_step=None) -> dict:
        """
        Execute the pipeline and return the final state dict.
        """
        state = {
            "uploaded_file": uploaded_file,
            "agent_log": [],
            "error": None,
        }

        pipeline = [
            self.file_detection,
            self.extraction,
            self.loading,
            self.understanding,
            self.cleaning,
            self.analysis,
            self.insight,
            self.visualization,
        ]

        for agent in pipeline:
            try:
                if callable(on_step):
                    on_step(agent.name)
                state = agent.run(state)
                if state.get("error"):
                    state["agent_log"].append(
                        f"❌ Pipeline stopped at {agent.name}: {state['error']}"
                    )
                    break
            except Exception as e:
                tb = traceback.format_exc()
                state["error"] = f"{agent.name} raised an exception: {e}"
                state["agent_log"].append(
                    f"❌ {agent.name} crashed:\n```\n{tb}\n```"
                )
                break

        state["pipeline_complete"] = state.get("error") is None
        return state

    def make_custom_chart(self, state: dict, chart_type: str, x_col: str,
                           y_col: str = None, color_col: str = None):
        """Generate a custom chart on demand from the UI."""
        df = state.get("clean_df")
        if df is None:
            return None
        return self.visualization.make_custom_chart(df, chart_type, x_col, y_col, color_col)
