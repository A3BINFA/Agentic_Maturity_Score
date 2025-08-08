![Alt Logo](Agentic_Maturity_Score/Riteupai_logo_august042025.png)

# Agentic Maturity Score (MVP)

An assessment tool and API that scores an organization's maturity against the Governance Agent Spec and generates a prioritized roadmap.

## Features
- **/assess**: Accept XLSX or JSON; returns domain scores, overall maturity, and a suggested roadmap.
- **/report**: Generate a polished PDF/DOCX report from assessment results.
- **/schema**: JSON Schemas for inputs/outputs.
- Excel **workbook** with auto-scoring columns and heatmaps (optional), and a CLI for local use.

## Quickstart
```bash
# 1) Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Run API
uvicorn agent.main:app --reload

# 3) Assess via curl (JSON)
curl -X POST http://localhost:8000/assess -H "Content-Type: application/json"   -d @samples/sample_input.json | jq .

# 4) Assess via curl (XLSX)
curl -X POST "http://localhost:8000/assess?format=xlsx"   -F "file=@workbook/Governance_Agent_Maturity_Toolkit.xlsx"

# 5) Generate PDF Report
curl -X POST http://localhost:8000/report -H "Content-Type: application/json"   -d @samples/sample_results.json --output out/report.pdf
```

## Docker
```bash
docker build -t agentic-maturity .
docker run -p 8000:8000 agentic-maturity
```

## Structure
```
agentic_maturity_score/
├── agent/               # FastAPI service
├── scoring/             # scoring logic
├── report/              # templates & renderers
├── schemas/             # pydantic models & JSON Schemas
├── workbook/            # Excel assessment workbook
├── cli/                 # CLI entry point
├── samples/             # sample input/result payloads
├── tests/               # pytest
└── infra/               # Dockerfile, CI workflow
```

## License
MIT
