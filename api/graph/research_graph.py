import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import TypedDict, List
from langgraph.graph import StateGraph, END

from agents.query_planner import run_query_planner
from agents.retriever import run_retriever
from agents.critical_analyst import run_critical_analyst
from agents.insight_generator import run_insight_generator
from agents.report_builder import run_report_builder

# ─────────────────────────────────────────────
# 1. DEFINE THE SHARED STATE
# This is the "baton" passed between all agents
# ─────────────────────────────────────────────
class ResearchState(TypedDict):
    topic: str              # User's research topic
    sub_queries: List[str]  # Agent 1 output
    raw_sources: List[dict] # Agent 2 output
    analysis: dict          # Agent 3 output
    insights: str           # Agent 4 output
    final_report: str       # Agent 5 output
    report_filename: str    # Saved file name


# ─────────────────────────────────────────────
# 2. DEFINE EACH NODE (one per agent)
# Each node receives state, does its job,
# returns updated state
# ─────────────────────────────────────────────

def node_query_planner(state: ResearchState) -> ResearchState:
    print("\n" + "="*50)
    print("AGENT 1: QUERY PLANNER")
    print("="*50)
    sub_queries = run_query_planner(state["topic"])
    return {"sub_queries": sub_queries}


def node_retriever(state: ResearchState) -> ResearchState:
    print("\n" + "="*50)
    print("AGENT 2: CONTEXTUAL RETRIEVER")
    print("="*50)
    raw_sources = run_retriever(state["sub_queries"])
    return {"raw_sources": raw_sources}


def node_critical_analyst(state: ResearchState) -> ResearchState:
    print("\n" + "="*50)
    print("AGENT 3: CRITICAL ANALYST")
    print("="*50)
    analysis = run_critical_analyst(state["raw_sources"])
    return {"analysis": analysis}


def node_insight_generator(state: ResearchState) -> ResearchState:
    print("\n" + "="*50)
    print("AGENT 4: INSIGHT GENERATOR")
    print("="*50)
    insights = run_insight_generator(state["topic"], state["analysis"])
    return {"insights": insights}


def node_report_builder(state: ResearchState) -> ResearchState:
    print("\n" + "="*50)
    print("AGENT 5: REPORT BUILDER")
    print("="*50)
    report, filename = run_report_builder(
        state["topic"],
        state["sub_queries"],
        state["analysis"],
        state["insights"],
        state["raw_sources"]
    )
    return {"final_report": report, "report_filename": filename}


# ─────────────────────────────────────────────
# 3. BUILD THE GRAPH
# ─────────────────────────────────────────────

def build_research_graph():
    # Create the graph with our state
    graph = StateGraph(ResearchState)
    
    # Add all 5 agent nodes
    graph.add_node("query_planner", node_query_planner)
    graph.add_node("retriever", node_retriever)
    graph.add_node("critical_analyst", node_critical_analyst)
    graph.add_node("insight_generator", node_insight_generator)
    graph.add_node("report_builder", node_report_builder)
    
    # Connect nodes in order (the relay race)
    graph.set_entry_point("query_planner")
    graph.add_edge("query_planner", "retriever")
    graph.add_edge("retriever", "critical_analyst")
    graph.add_edge("critical_analyst", "insight_generator")
    graph.add_edge("insight_generator", "report_builder")
    graph.add_edge("report_builder", END)
    
    # Compile and return
    return graph.compile()


def run_research(topic: str) -> dict:
    """Main function — takes a topic, runs all agents, returns final state"""
    
    print("\n" + "🚀 "*10)
    print(f"STARTING MULTI-AGENT RESEARCH")
    print(f"TOPIC: {topic}")
    print("🚀 "*10)
    
    # Build the graph
    app = build_research_graph()
    
    # Set initial state
    initial_state = {
        "topic": topic,
        "sub_queries": [],
        "raw_sources": [],
        "analysis": {},
        "insights": "",
        "final_report": "",
        "report_filename": ""
    }
    
    # Run the full pipeline
    final_state = app.invoke(initial_state)
    
    print("\n" + "✅ "*10)
    print("RESEARCH COMPLETE!")
    print(f"Report saved as: {final_state['report_filename']}")
    print("✅ "*10)
    
    return final_state


# Test the full pipeline
if __name__ == "__main__":
    result = run_research("Full analysis on SpaceX's IPO and what it means for the retail investors who bought in during the hype")
    
    print("\n--- FINAL REPORT PREVIEW ---")
    print(result["final_report"][:800])
    print("\n... (full report saved to file)")