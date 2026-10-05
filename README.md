# BankAI Assistant Lab

A portfolio-grade AI Engineering sandbox for a banking customer-support assistant. It demonstrates an observable agent workflow without pretending to connect to a real bank.

## Current implementation
- Python + FastAPI backend
- Deterministic intent router
- Mock banking tools: balance, transaction lookup, card status, branch search
- Lightweight knowledge retrieval from a seeded FAQ set
- Safety checks for sensitive credential requests
- Evaluation harness with correctness, safety and groundedness metrics
- Responsive frontend with Chat, Workflow, Evaluation and About views

## Planned production extensions
- Real LLM API (OpenAI/Anthropic/etc.)
- LangGraph stateful orchestration
- MCP server/tool integration
- RAG with embeddings and a vector database
- PostgreSQL persistence
- Model-based LLM evaluation
- STT/TTS voice assistant
- Authentication and real banking integrations behind appropriate security controls

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

## Portfolio note
This project intentionally uses mock data. It is a learning/portfolio project and is not a real banking service.
