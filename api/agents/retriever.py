import sys
import os

from tavily import TavilyClient
from config import TAVILY_API_KEY

# Connect to Tavily
tavily = TavilyClient(api_key=TAVILY_API_KEY)

def run_retriever(sub_queries: list) -> list:
    """Takes a list of questions, searches the web for each, returns all results"""
    
    print(f"\n🌐 Retriever: Searching web for {len(sub_queries)} questions...")
    
    all_sources = []
    
    for i, query in enumerate(sub_queries, 1):
        print(f"\n   🔎 Searching ({i}/{len(sub_queries)}): {query}")
        
        try:
            # Search Tavily for this question
            # max_results=3 means we get 3 articles per question
            response = tavily.search(
                query=query,
                max_results=3,
                search_depth="basic"
            )
            
            # Extract the results
            results = response.get("results", [])
            
            for result in results:
                source = {
                    "query": query,
                    "title": result.get("title", "No title"),
                    "url": result.get("url", "No URL"),
                    "content": result.get("content", "No content"),
                    "score": result.get("score", 0)
                }
                all_sources.append(source)
                print(f"      ✅ Found: {source['title'][:60]}...")
                
        except Exception as e:
            print(f"      ❌ Search failed for this query: {e}")
            continue
    
    print(f"\n📚 Retriever: Collected {len(all_sources)} total sources")
    return all_sources


# Test this agent alone
if __name__ == "__main__":
    # Simulate what Query Planner would pass
    test_queries = [
        "What jobs are currently being replaced by AI?",
        "What new jobs is AI creating in the workforce?"
    ]
    
    results = run_retriever(test_queries)
    
    print("\n--- SAMPLE SOURCE ---")
    if results:
        print(f"Title: {results[0]['title']}")
        print(f"URL: {results[0]['url']}")
        print(f"Content preview: {results[0]['content'][:200]}...")
        