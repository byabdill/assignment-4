import os
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
import prompts

load_dotenv()

# 1. СТРУКТУРЫ ДАННЫХ
class PlayerMetrics(BaseModel):
    player_name: str
    pace: int = Field(description="Speed 1-10")
    passing: int = Field(description="Passing 1-10")
    shooting: int = Field(description="Shooting 1-10")
    stamina: int = Field(description="Stamina 1-10")

class ScoutReport(BaseModel):
    decision: str = Field(description="Sign, Monitor, or Reject")
    estimated_value: str
    justification: str

class AgentState(BaseModel):
    text_input: str
    metrics: Optional[PlayerMetrics] = None
    report: Optional[ScoutReport] = None

# 2. ИНИЦИАЛИЗАЦИЯ LLM
# Убедись, что в .env есть GOOGLE_API_KEY
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# 3. УЗЛЫ ГРАФА
def node_parse_text(state: AgentState):
    print("--- Узел 1: Обработка текста ---")
    return {"text_input": state.text_input.strip()}

def node_extract_metrics(state: AgentState):
    print("--- Узел 2: Извлечение метрик (LLM 1) ---")
    structured_llm = llm.with_structured_output(PlayerMetrics)
    res = structured_llm.invoke(prompts.ANALYST_PROMPT.format(input_text=state.text_input))
    return {"metrics": res}

def node_generate_report(state: AgentState):
    print("--- Узел 3: Финальный вердикт (LLM 2) ---")
    structured_llm = llm.with_structured_output(ScoutReport)
    res = structured_llm.invoke(
        prompts.SCOUT_PROMPT.format(
            player_name=state.metrics.player_name,
            metrics=state.metrics.dict()
        )
    )
    return {"report": res}

# 4. СБОРКА ГРАФА
builder = StateGraph(AgentState)
builder.add_node("ingest", node_parse_text)
builder.add_node("analyst", node_extract_metrics)
builder.add_node("scout", node_generate_report)

builder.set_entry_point("ingest")
builder.add_edge("ingest", "analyst")
builder.add_edge("analyst", "scout")
builder.add_edge("scout", END)

app = builder.compile()

# ТЕСТОВЫЙ ЗАПУСК
if __name__ == "__main__":
    raw_data = "Erling Haaland was unstoppable today. His speed is a 10, finishing is 10, but passing is around 7."
    result = app.invoke({"text_input": raw_data})
    
    print("\n=== FINAL SCOUT REPORT ===")
    print(f"Player: {result['metrics'].player_name}")
    print(f"Decision: {result['report'].decision}")
    print(f"Value: {result['report'].estimated_value}")
    print(f"Summary: {result['report'].justification}")