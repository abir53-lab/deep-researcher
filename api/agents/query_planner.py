import sys
import os

# This tells Python to look in the root project folder for config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL_NAME

# This sets up the LLM connection via OpenRouter
llm = ChatOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    model=MODEL_NAME
)

# This is the instruction we give the LLM
prompt = ChatPromptTemplate.from_template("""
You are a research planning expert. 
A user wants to research this topic: {topic}

Your job is to break this into exactly 4 specific search questions.
These questions should cover different angles of the topic.

Return ONLY a Python list of 4 questions like this format:
["question 1", "question 2", "question 3", "question 4"]

Do not add any explanation. Just the list.
""")

def run_query_planner(topic: str) -> list:
    """Takes a topic string, returns a list of 4 sub-questions"""
    
    print(f"\n🔍 Query Planner: Breaking down topic: '{topic}'")
    
    # Format the prompt with the actual topic
    formatted_prompt = prompt.format_messages(topic=topic)
    
    # Send to LLM and get response
    response = llm.invoke(formatted_prompt)
    
    # The response comes back as text - we need to convert it to a Python list
    raw_text = response.content.strip()
    
    # Safely convert the text list into a real Python list
    import ast
    try:
        sub_queries = ast.literal_eval(raw_text)
        print(f"✅ Generated {len(sub_queries)} sub-questions:")
        for i, q in enumerate(sub_queries, 1):
            print(f"   {i}. {q}")
        return sub_queries
    except:
        # If LLM didn't follow format exactly, split by newlines as backup
        print("⚠️  Parsing fallback used")
        lines = [line.strip().strip('"') for line in raw_text.split('\n') if line.strip()]
        return lines[:4]

# Test this agent alone
if __name__ == "__main__":
    topic = "Impact of artificial intelligence on jobs"
    result = run_query_planner(topic)
    print("\n📋 Final sub-queries:", result)