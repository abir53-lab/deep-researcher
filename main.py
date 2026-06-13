import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph.research_graph import run_research

def print_banner():
    print("\n")
    print("=" * 60)
    print("   🧠  MULTI-AGENT AI DEEP RESEARCHER")
    print("   Built with LangGraph + DeepSeek + Tavily")
    print("=" * 60)
    print("   Agents:")
    print("   1️⃣  Query Planner    → Breaks topic into sub-questions")
    print("   2️⃣  Retriever        → Searches web via Tavily")
    print("   3️⃣  Critical Analyst → Summarizes + finds contradictions")
    print("   4️⃣  Insight Generator→ Finds trends + hypotheses")
    print("   5️⃣  Report Builder   → Compiles final report")
    print("=" * 60)
    print()

def get_user_topic() -> str:
    print("Enter your research topic below.")
    print("Example: 'Impact of AI on healthcare'")
    print("Example: 'Future of electric vehicles'")
    print("Example: 'Climate change solutions'")
    print()
    topic = input("🔬 Your research topic: ").strip()
    
    if not topic:
        print("❌ No topic entered. Please try again.")
        sys.exit(1)
    
    return topic

def display_report_summary(final_state: dict):
    print("\n")
    print("=" * 60)
    print("   📊 RESEARCH SUMMARY")
    print("=" * 60)
    print(f"   Topic    : {final_state['topic']}")
    print(f"   Questions: {len(final_state['sub_queries'])} sub-questions investigated")
    print(f"   Sources  : {len(final_state['raw_sources'])} web sources retrieved")
    print(f"   Report   : {final_state['report_filename']}")
    print("=" * 60)
    
    # Ask if user wants to preview the report
    print()
    preview = input("👀 Preview report in terminal? (y/n): ").strip().lower()
    
    if preview == "y":
        print("\n")
        print("=" * 60)
        print("   📄 REPORT PREVIEW")
        print("=" * 60)
        print(final_state["final_report"][:2000])
        print("\n... (full report saved to file, open it in VS Code)")
    
    print()
    print("✅ Done! Open your report file in VS Code to read the full version.")
    print(f"📁 File: {final_state['report_filename']}")
    print()

def main():
    # Show the banner
    print_banner()
    
    # Get topic from user
    topic = get_user_topic()
    
    # Confirm before running
    print()
    print(f"📌 Topic confirmed: '{topic}'")
    print("⏱️  Estimated time: 60-120 seconds")
    print()
    confirm = input("🚀 Start research? (y/n): ").strip().lower()
    
    if confirm != "y":
        print("Research cancelled.")
        sys.exit(0)
    
    # Track start time
    start_time = datetime.now()
    
    # Run the full multi-agent pipeline
    try:
        final_state = run_research(topic)
        
        # Calculate how long it took
        end_time = datetime.now()
        duration = (end_time - start_time).seconds
        
        print(f"\n⏱️  Total research time: {duration} seconds")
        
        # Show summary
        display_report_summary(final_state)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Research interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during research: {e}")
        print("Check your API keys in .env file and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()