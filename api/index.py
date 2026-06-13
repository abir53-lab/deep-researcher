import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from graph.research_graph import run_research
app = FastAPI()
class ResearchRequest(BaseModel):
    topic: str
@app.get("/", response_class=HTMLResponse)
async def root():
    static_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "index.html")
    with open(static_path, "r") as f:
        return f.read()
@app.post("/api/research")
async def research(request: ResearchRequest):
    try:
        if not request.topic.strip():
            return JSONResponse(status_code=400, content={"error": "Topic cannot be empty"})
        final_state = run_research(request.topic)
        return JSONResponse(content={
            "success": True,
            "topic": final_state["topic"],
            "sub_queries": final_state["sub_queries"],
            "sources_count": len(final_state["raw_sources"]),
            "report": final_state["final_report"],
            "filename": final_state["report_filename"]
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
@app.get("/health")
async def health():
    return {"status": "ok"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
