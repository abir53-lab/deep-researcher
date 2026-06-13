import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph.research_graph import run_research

# ─────────────────────────────────────────────
# HACKATHON DEMO SCRIPT
# Runs automatically — no input needed
# Perfect for live presentations
# ─────────────────────────────────────────────

DEMO_TOPIC = "The future of AI agents in the workplace by 2030"

def print_demo_banner():
    print("\n")
    print("🎯 " * 20)
    print()
    print("   MULTI-AGENT AI DEEP RESEARCHER")
    print("   LIVE HACKATHON DEMO")
    print()
    print("🎯 " * 20)
    print()
    print("   TECH STACK:")
    print("   ├── 🧠 LLM        : DeepSeek V3 via OpenRouter")
    print("   ├── 🔍 Search     : Tavily Web Search API")
    print("   ├── 🔗 Orchestration: LangGraph")
    print("   └── 🐍 Language   : Python 3.9")
    print()
    print("   AGENT PIPELINE:")
    print("   Query Planner → Retriever → Critical Analyst")
    print("   → Insight Generator → Report Builder")
    print()
    print("🎯 " * 20)
    print()
    print(f"   📌 DEMO TOPIC:")
    print(f"   '{DEMO_TOPIC}'")
    print()
    print("🎯 " * 20)
    print()

def main():
    print_demo_banner()
    
    print("⏳ Starting research pipeline in 3 seconds...")
    import time
    time.sleep(3)
    
    start_time = datetime.now()
    
    try:
        # Run the full pipeline
        final_state = run_research(DEMO_TOPIC)
        
        end_time = datetime.now()
        duration = (end_time - start_time).seconds
        
        # Print impressive summary
        print("\n")
        print("🏆 " * 20)
        print()
        print("   RESEARCH COMPLETE!")
        print()
        print(f"   ⏱️  Time taken     : {duration} seconds")
        print(f"   ❓ Sub-questions  : {len(final_state['sub_queries'])}")
        print(f"   📚 Sources found  : {len(final_state['raw_sources'])}")
        print(f"   📄 Report saved   : {final_state['report_filename']}")
        print()
        print("🏆 " * 20)
        
        # Print report preview
        print("\n")
        print("=" * 60)
        print("   📄 REPORT PREVIEW (first 1500 characters)")
        print("=" * 60)
        print()
        print(final_state["final_report"][:1500])
        print()
        print("... (full report saved to file)")
        print()
        print("=" * 60)
        print("   🎯 END OF DEMO")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()