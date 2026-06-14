import os
import sys

# Vercel fix - add api folder to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typing import TypedDict, List
from langgraph.graph import StateGraph, END

from agents.query_planner import run_query_planner
from agents.retriever import run_retriever
from agents.critical_analyst import run_critical_analyst
from agents.insight_generator import run_insight_generator
from agents.report_builder import run_report_builder

class ResearchState(TypedDict):
    topic: str
    sub_queries: List[str]
    raw_sources: List[dict]
    analysis: dict
    insights: str
    final_report: str
    report_filename: str

def node_query_planner(state: ResearchState) -> ResearchState:
    print("AGENT 1: QUERY PLANNER")
    sub_queries = run_query_planner(state["topic"])
    return {"sub_queries": sub_queries}

def node_retriever(state: ResearchState) -> ResearchState:
    print("AGENT 2: RETRIEVER")
    raw_sources = run_retriever(state["sub_queries"])
    return {"raw_sources": raw_sources}

def node_critical_analyst(state: ResearchState) -> ResearchState:
    print("AGENT 3: CRITICAL ANALYST")
    analysis = run_critical_analyst(state["raw_sources"])
    return {"analysis": analysis}

def node_insight_generator(state: ResearchState) -> ResearchState:
    print("AGENT 4: INSIGHT GENERATOR")
    insights = run_insight_generator(state["topic"], state["analysis"])
    return {"insights": insights}

def node_report_builder(state: ResearchState) -> ResearchState:
    print("AGENT 5: REPORT BUILDER")
    report, filename = run_report_builder(
        state["topic"],
        state["sub_queries"],
        state["analysis"],
        state["insights"],
        state["raw_sources"]
    )
    return {"final_report": report, "report_filename": filename}

def build_research_graph():
    graph = StateGraph(ResearchState)
    graph.add_node("query_planner", node_query_planner)
    graph.add_node("retriever", node_retriever)
    graph.add_node("critical_analyst", node_critical_analyst)
    graph.add_node("insight_generator", node_insight_generator)
    graph.add_node("report_builder", node_report_builder)
    graph.set_entry_point("query_planner")
    graph.add_edge("query_planner", "retriever")
    graph.add_edge("retriever", "critical_analyst")
    graph.add_edge("critical_analyst", "insight_generator")
    graph.add_edge("insight_generator", "report_builder")
    graph.add_edge("report_builder", END)
    return graph.compile()

def run_research(topic: str) -> dict:
    print(f"STARTING RESEARCH: {topic}")
    app = build_research_graph()
    initial_state = {
        "topic": topic,
        "sub_queries": [],
        "raw_sources": [],
        "analysis": {},
        "insights": "",
        "final_report": "",
        "report_filename": ""
    }
    final_state = app.invoke(initial_state)
    print("RESEARCH COMPLETE")
    return final_state
