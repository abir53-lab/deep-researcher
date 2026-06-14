import sys
import os

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL_NAME

# Connect to LLM
llm = ChatOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    model=MODEL_NAME
)

# Prompt for summarizing sources
summary_prompt = ChatPromptTemplate.from_template("""
You are a critical research analyst. 
Analyze these search results about: {query}

Sources:
{sources}

Your job:
1. Write a 2-3 sentence summary of the key finding from these sources
2. Note the credibility of the sources (high/medium/low)
3. Highlight any surprising or important facts

Return your response in this exact format:
SUMMARY: [your 2-3 sentence summary]
CREDIBILITY: [high/medium/low]
KEY FACT: [one most important fact]
""")

# Prompt for finding contradictions across all sources
contradiction_prompt = ChatPromptTemplate.from_template("""
You are a critical research analyst.
Review these research findings from multiple sources:

{all_summaries}

Your job:
1. Find where sources AGREE with each other
2. Find where sources CONTRADICT or DISAGREE with each other
3. Flag any claims that seem uncertain or need more evidence

Return your response in this exact format:
AGREEMENTS: [list the main points sources agree on]
CONTRADICTIONS: [list where sources disagree - if none write "No major contradictions found"]
UNCERTAIN CLAIMS: [list claims that need more evidence]
""")


def run_critical_analyst(sources: list) -> dict:
    """Takes raw sources, returns summaries and contradiction analysis"""
    
    print(f"\n🔬 Critical Analyst: Analyzing {len(sources)} sources...")
    
    # Group sources by their original query
    sources_by_query = {}
    for source in sources:
        query = source["query"]
        if query not in sources_by_query:
            sources_by_query[query] = []
        sources_by_query[query].append(source)
    
    # Summarize each group of sources
    summaries = []
    
    for query, query_sources in sources_by_query.items():
        print(f"\n   📖 Analyzing sources for: {query[:60]}...")
        
        # Format sources for the prompt
        sources_text = ""
        for i, s in enumerate(query_sources, 1):
            sources_text += f"\nSource {i}: {s['title']}\n"
            sources_text += f"URL: {s['url']}\n"
            sources_text += f"Content: {s['content'][:500]}\n"
            sources_text += "---"
        
        # Ask LLM to analyze
        formatted_prompt = summary_prompt.format_messages(
            query=query,
            sources=sources_text
        )
        response = llm.invoke(formatted_prompt)
        
        summary_entry = {
            "query": query,
            "analysis": response.content.strip()
        }
        summaries.append(summary_entry)
        print(f"   ✅ Analysis complete for this query")
    
    # Now find contradictions across ALL summaries
    print(f"\n   🔍 Finding contradictions across all sources...")
    
    all_summaries_text = ""
    for s in summaries:
        all_summaries_text += f"\nQuery: {s['query']}\n"
        all_summaries_text += f"Analysis: {s['analysis']}\n"
        all_summaries_text += "---\n"
    
    contradiction_formatted = contradiction_prompt.format_messages(
        all_summaries=all_summaries_text
    )
    contradiction_response = llm.invoke(contradiction_formatted)
    
    result = {
        "summaries": summaries,
        "contradictions": contradiction_response.content.strip()
    }
    
    print(f"✅ Critical Analyst complete")
    return result


# Test this agent alone
if __name__ == "__main__":
    # Simulate what Retriever would pass
    test_sources = [
        {
            "query": "What jobs are currently being replaced by AI?",
            "title": "AI is replacing customer service jobs fast",
            "url": "https://example.com/1",
            "content": "AI has already replaced millions of customer service roles. Chatbots now handle 70% of basic customer inquiries. However, complex problem-solving roles remain human-dominated.",
            "score": 0.9
        },
        {
            "query": "What jobs are currently being replaced by AI?",
            "title": "AI creates more jobs than it destroys says new report",
            "url": "https://example.com/2",
            "content": "A new LinkedIn report suggests AI has created 1.3 million new jobs while displacing 800,000. Net job creation is positive according to this analysis.",
            "score": 0.85
        },
        {
            "query": "What new jobs is AI creating?",
            "title": "The rise of AI trainers and prompt engineers",
            "url": "https://example.com/3",
            "content": "New roles like AI trainer, prompt engineer, and AI ethicist are emerging. Companies are hiring humans to supervise and improve AI systems.",
            "score": 0.88
        }
    ]
    
    result = run_critical_analyst(test_sources)
    
    print("\n--- SUMMARIES ---")
    for s in result["summaries"]:
        print(f"\nQuery: {s['query'][:60]}...")
        print(s["analysis"])
    
    print("\n--- CONTRADICTIONS ---")
    print(result["contradictions"])