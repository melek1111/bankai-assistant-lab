from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .agent import run_agent
from .evaluation import evaluate_cases

app = FastAPI(title="BankAI Assistant Lab", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "portfolio-demo", "real_bank_integration": False}

@app.post("/api/chat")
def chat(req: ChatRequest):
    return run_agent(req.message)

@app.get("/api/evaluation")
def evaluation():
    return evaluate_cases()
