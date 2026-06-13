import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL_NAME

# Connect to LLM
llm = ChatOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    model=MODEL_NAME
)

insight_prompt = ChatPromptTemplate.from_template("""
You are a senior research analyst and futurist.
You have been given research findings and contradiction analysis on this topic: {topic}

Research Summaries:
{summaries}

Contradiction Analysis:
{contradictions}

Your job is to think ACROSS all this information and generate:
1. KEY TRENDS: What patterns are emerging from all this research?
2. HYPOTHESES: What educated predictions can you make based on evidence?
3. IMPLICATIONS: What does this mean for people, organizations, or society?
4. OPEN QUESTIONS: What important questions remain unanswered?
5. SURPRISING INSIGHT: What is one non-obvious insight from all this research?

Be specific. Reference the research findings when making claims.
Think like a McKinsey consultant writing for a CEO.

Format your response exactly like this:

KEY TRENDS:
- [trend 1]
- [trend 2]
- [trend 3]

HYPOTHESES:
- [hypothesis 1]
- [hypothesis 2]

IMPLICATIONS:
- [implication 1]
- [implication 2]
- [implication 3]

OPEN QUESTIONS:
- [question 1]
- [question 2]

SURPRISING INSIGHT:
[one paragraph with your most non-obvious insight]
""")


def run_insight_generator(topic: str, analysis: dict) -> str:
    """Takes topic + analysis dict, returns structured insights"""
    
    print(f"\n💡 Insight Generator: Synthesizing insights for '{topic}'...")
    
    # Format summaries for prompt
    summaries_text = ""
    for s in analysis["summaries"]:
        summaries_text += f"\nResearch Area: {s['query']}\n"
        summaries_text += f"{s['analysis']}\n"
        summaries_text += "---\n"
    
    # Format the prompt
    formatted_prompt = insight_prompt.format_messages(
        topic=topic,
        summaries=summaries_text,
        contradictions=analysis["contradictions"]
    )
    
    # Send to LLM
    response = llm.invoke(formatted_prompt)
    insights = response.content.strip()
    
    print("✅ Insights generated successfully")
    return insights


# Test this agent alone
if __name__ == "__main__":
    # Simulate what Critical Analyst would pass
    test_topic = "Impact of artificial intelligence on jobs"
    
    test_analysis = {
        "summaries": [
            {
                "query": "What jobs are currently being replaced by AI?",
                "analysis": """SUMMARY: AI is rapidly replacing customer service jobs, with chatbots handling 70% of basic inquiries. However LinkedIn data shows AI created 1.3M jobs while displacing 800K.
CREDIBILITY: medium
KEY FACT: Net job creation is positive at +500,000 jobs despite displacement."""
            },
            {
                "query": "What new jobs is AI creating?",
                "analysis": """SUMMARY: New roles like AI trainer, prompt engineer, and AI ethicist are emerging as companies hire humans to supervise AI systems.
CREDIBILITY: medium
KEY FACT: Human oversight roles are growing fastest in the AI job market."""
            }
        ],
        "contradictions": """AGREEMENTS:
- Both sources agree AI is transforming jobs significantly
- New human oversight roles are emerging

CONTRADICTIONS:
- No major contradictions found

UNCERTAIN CLAIMS:
- The 1.3M job creation figure lacks methodological detail
- 70% chatbot statistic lacks direct attribution"""
    }
    
    insights = run_insight_generator(test_topic, test_analysis)
    
    print("\n--- INSIGHTS ---")
    print(insights)