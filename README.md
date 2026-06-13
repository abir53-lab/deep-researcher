# 🧠 Multi-Agent AI Deep Researcher

> An AI-powered research assistant that spins up 5 specialized agents to investigate any topic — pulling live web data, analyzing contradictions, generating insights, and compiling a structured report automatically.

---

## 🎯 What It Does

You type a research topic. Five AI agents collaborate to produce a full research report in under 2 minutes.
---

## 🤖 The 5 Agents

| Agent | Job |
|---|---|
| 🗺️ Query Planner | Breaks topic into 4 targeted sub-questions |
| 🌐 Contextual Retriever | Searches live web via Tavily for each question |
| 🔬 Critical Analyst | Summarizes sources, scores credibility, flags contradictions |
| 💡 Insight Generator | Synthesizes trends, hypotheses and implications |
| 📝 Report Builder | Compiles everything into a structured markdown report |

---

## 🛠️ Tech Stack

- **Language:** Python 3.9
- **Agent Orchestration:** LangGraph
- **LLM:** DeepSeek V3 via OpenRouter
- **Web Search:** Tavily Search API
- **Prompt Management:** LangChain

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/deep_researcher.git
cd deep_researcher
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API keys
```bash
cp .env.example .env
# Edit .env and add your keys
```

### 5. Run the app
```bash
python3 main.py
```

### 6. Run the demo
```bash
python3 demo.py
```

---

## 📁 Project Structure
---

## 🔑 Environment Variables

Create a .env file in the root folder:
Get your keys here:
- OpenRouter: https://openrouter.ai
- Tavily: https://tavily.com

---

## 📄 Sample Report Output

Every run generates a timestamped markdown report containing:

- Executive Summary
- Research Scope (4 sub-questions investigated)
- Key Findings per sub-question with facts and figures
- Contradictions and Uncertainties between sources
- Insights and Trends synthesized across all sources
- Hypotheses based on evidence
- Implications for individuals, organizations, and policymakers
- Open Questions for further research
- Full source citations with URLs

---

## 🏗️ How The Agents Collaborate
---

## 🎯 Example Topics To Try

- "Impact of artificial intelligence on jobs"
- "Future of electric vehicles by 2030"
- "Climate change solutions and their effectiveness"
- "The rise of remote work after COVID-19"
- "Quantum computing breakthroughs in 2024"

---

## ⏱️ Performance

| Metric | Value |
|---|---|
| Average research time | 60-120 seconds |
| Sub-questions per topic | 4 |
| Web sources retrieved | 12 |
| LLM calls per run | 7-8 |
| Output format | Markdown (.md) |

---

## 🙏 Built With

- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [LangChain](https://github.com/langchain-ai/langchain) - LLM framework
- [OpenRouter](https://openrouter.ai) - LLM API gateway
- [DeepSeek V3](https://deepseek.com) - Large language model
- [Tavily](https://tavily.com) - AI-optimized web search

---

*Built for hackathon — Multi-Agent AI Deep Researcher*
*Powered by 5 collaborating AI agents*
