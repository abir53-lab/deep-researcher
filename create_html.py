import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Multi-Agent AI Deep Researcher</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: sans-serif; background: #0d1117; color: #e6edf3; min-height: 100vh; }
header { background: #161b22; border-bottom: 1px solid #30363d; padding: 20px 40px; }
header h1 { font-size: 22px; color: #58a6ff; }
header p { font-size: 13px; color: #8b949e; margin-top: 4px; }
.container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
.search-box { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 32px; margin-bottom: 32px; }
.search-box label { display: block; font-size: 14px; color: #8b949e; margin-bottom: 12px; }
.search-row { display: flex; gap: 12px; }
.search-row input { flex: 1; background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; color: #e6edf3; font-size: 15px; outline: none; }
.search-row button { background: #1f6feb; color: white; border: none; border-radius: 8px; padding: 12px 28px; font-size: 15px; font-weight: 600; cursor: pointer; }
.search-row button:disabled { background: #30363d; cursor: not-allowed; }
.pipeline { display: none; background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 24px; margin-bottom: 32px; }
.pipeline h3 { font-size: 14px; color: #8b949e; margin-bottom: 20px; }
.agent-steps { display: flex; flex-direction: column; gap: 12px; }
.agent-step { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: #0d1117; border-radius: 8px; border: 1px solid #30363d; opacity: 0.4; transition: all 0.3s; }
.agent-step.active { opacity: 1; border-color: #1f6feb; }
.agent-step.done { opacity: 1; border-color: #3fb950; }
.step-icon { font-size: 20px; }
.step-name { font-size: 14px; font-weight: 600; flex: 1; }
.step-status { font-size: 12px; color: #8b949e; }
.step-status.running { color: #58a6ff; }
.step-status.done { color: #3fb950; }
.report-box { display: none; background: #161b22; border: 1px solid #3fb950; border-radius: 12px; padding: 32px; }
.report-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #30363d; }
.report-header h2 { color: #3fb950; font-size: 18px; }
.report-stats { display: flex; gap: 16px; }
.stat { text-align: center; background: #0d1117; border-radius: 8px; padding: 8px 16px; }
.stat .number { font-size: 20px; font-weight: 700; color: #58a6ff; }
.stat .label { font-size: 11px; color: #8b949e; margin-top: 2px; }
.report-content { background: #0d1117; border-radius: 8px; padding: 24px; white-space: pre-wrap; font-family: monospace; font-size: 13px; line-height: 1.7; max-height: 600px; overflow-y: auto; }
.download-btn { margin-top: 16px; background: #238636; color: white; border: none; border-radius: 8px; padding: 10px 24px; font-size: 14px; font-weight: 600; cursor: pointer; }
.error-box { display: none; background: #2d1318; border: 1px solid #f85149; border-radius: 12px; padding: 24px; color: #f85149; margin-bottom: 32px; }
footer { text-align: center; padding: 32px; color: #8b949e; font-size: 12px; border-top: 1px solid #30363d; margin-top: 40px; }
</style>
</head>
<body>
<header>
<h1>🧠 Multi-Agent AI Deep Researcher</h1>
<p>5 AI agents collaborate to research any topic and generate a structured report</p>
</header>
<div class="container">
<div class="search-box">
<label>Enter your research topic</label>
<div class="search-row">
<input type="text" id="topicInput" placeholder="e.g. Impact of AI on jobs in 2025"/>
<button id="researchBtn" onclick="startResearch()">🔍 Research</button>
</div>
</div>
<div class="pipeline" id="pipeline">
<h3>⚡ Agent Pipeline Running</h3>
<div class="agent-steps">
<div class="agent-step" id="step1"><span class="step-icon">🗺️</span><span class="step-name">Query Planner</span><span class="step-status" id="status1">Waiting...</span></div>
<div class="agent-step" id="step2"><span class="step-icon">🌐</span><span class="step-name">Contextual Retriever</span><span class="step-status" id="status2">Waiting...</span></div>
<div class="agent-step" id="step3"><span class="step-icon">🔬</span><span class="step-name">Critical Analyst</span><span class="step-status" id="status3">Waiting...</span></div>
<div class="agent-step" id="step4"><span class="step-icon">💡</span><span class="step-name">Insight Generator</span><span class="step-status" id="status4">Waiting...</span></div>
<div class="agent-step" id="step5"><span class="step-icon">📝</span><span class="step-name">Report Builder</span><span class="step-status" id="status5">Waiting...</span></div>
</div>
</div>
<div class="error-box" id="errorBox"><strong>Error:</strong> <span id="errorMsg"></span></div>
<div class="report-box" id="reportBox">
<div class="report-header">
<h2>✅ Research Complete</h2>
<div class="report-stats">
<div class="stat"><div class="number" id="statQuestions">4</div><div class="label">Questions</div></div>
<div class="stat"><div class="number" id="statSources">12</div><div class="label">Sources</div></div>
</div>
</div>
<div class="report-content" id="reportContent"></div>
<button class="download-btn" onclick="downloadReport()">Download Report</button>
</div>
</div>
<footer>Built with LangGraph · DeepSeek V3 · Tavily · Python</footer>
<script>
let currentReport = "";
function animateSteps() {
  const labels = ["Breaking topic into questions...","Searching the web...","Analyzing sources...","Generating insights...","Building report..."];
  const times = [0, 15000, 35000, 55000, 75000];
  labels.forEach((label, i) => {
    setTimeout(() => {
      if (i > 0) {
        document.getElementById("step"+i).className = "agent-step done";
        document.getElementById("status"+i).textContent = "Done";
        document.getElementById("status"+i).className = "step-status done";
      }
      document.getElementById("step"+(i+1)).className = "agent-step active";
      document.getElementById("status"+(i+1)).textContent = label;
      document.getElementById("status"+(i+1)).className = "step-status running";
    }, times[i]);
  });
}
async function startResearch() {
  const topic = document.getElementById("topicInput").value.trim();
  if (!topic) { alert("Please enter a research topic first"); return; }
  document.getElementById("reportBox").style.display = "none";
  document.getElementById("errorBox").style.display = "none";
  document.getElementById("pipeline").style.display = "block";
  document.getElementById("researchBtn").disabled = true;
  document.getElementById("researchBtn").textContent = "Researching...";
  for (let i = 1; i <= 5; i++) {
    document.getElementById("step"+i).className = "agent-step";
    document.getElementById("status"+i).textContent = "Waiting...";
    document.getElementById("status"+i).className = "step-status";
  }
  animateSteps();
  try {
    const response = await fetch("/api/research", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic: topic })
    });
    const data = await response.json();
    for (let i = 1; i <= 5; i++) {
      document.getElementById("step"+i).className = "agent-step done";
      document.getElementById("status"+i).textContent = "Done";
      document.getElementById("status"+i).className = "step-status done";
    }
    if (data.success) {
      currentReport = data.report;
      document.getElementById("statQuestions").textContent = data.sub_queries.length;
      document.getElementById("statSources").textContent = data.sources_count;
      document.getElementById("reportContent").textContent = data.report;
      document.getElementById("reportBox").style.display = "block";
    } else { throw new Error(data.error || "Research failed"); }
  } catch (error) {
    document.getElementById("errorMsg").textContent = error.message;
    document.getElementById("errorBox").style.display = "block";
  } finally {
    document.getElementById("researchBtn").disabled = false;
    document.getElementById("researchBtn").textContent = "🔍 Research";
  }
}
function downloadReport() {
  const blob = new Blob([currentReport], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "research_report.md";
  a.click();
  URL.revokeObjectURL(url);
}
</script>
</body>
</html>"""

os.makedirs("static", exist_ok=True)
with open("static/index.html", "w") as f:
    f.write(html_content)

print("SUCCESS!")
print("File size:", os.path.getsize("static/index.html"), "bytes")