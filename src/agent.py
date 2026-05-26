from typing import TypedDict, Optional, Dict, Any
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from src.database import get_schema_string, run_read_only_query
import pandas as pd

# 1. Enforced Pydantic Schemas for LLM Output
class SQLGenerationPayload(BaseModel):
    sql_query: str = Field(description="The valid SQLite query to execute.")
    explanation: str = Field(description="Brief explanation of the logic behind the SQL query.")

class VisualizationPayload(BaseModel):
    summary: str = Field(description="Executive summary of the quantitative results.")
    chart_type: str = Field(description="Best visualization type: 'bar', 'line', or 'none'.")
    x_column: Optional[str] = Field(description="Column name to place on the X axis.")
    y_column: Optional[str] = Field(description="Column name to place on the Y axis.")

# 2. State definition tracking execution across the graph
class AgentState(TypedDict):
    user_query: str
    schema_context: str
    generated_sql: Optional[str]
    sql_explanation: Optional[str]
    query_result: Optional[pd.DataFrame]
    error_message: Optional[str]
    retry_count: int
    final_summary: Optional[str]
    chart_metadata: Optional[Dict[str, Any]]
