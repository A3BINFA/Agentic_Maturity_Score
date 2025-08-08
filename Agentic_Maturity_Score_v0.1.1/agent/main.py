from fastapi import FastAPI, UploadFile, File, Query, Response
from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import pandas as pd
from io import BytesIO
from scoring.core import assess_dataframe, assess_json
from schemas.io import AssessmentInput, AssessmentResult, get_schemas
from report.render import render_pdf_bytes, render_docx_bytes

app = FastAPI(title="Agentic Maturity Score", version="0.1.0")

@app.get("/schema")
def schema() -> Dict[str, Any]:
    return get_schemas()

@app.post("/assess", response_model=AssessmentResult)
async def assess(
    payload: Optional[AssessmentInput] = None,
    file: Optional[UploadFile] = File(default=None),
    format: str = Query("json", enum=["json","xlsx"]),
):
    try:
        if format == "xlsx":
            if file is None:
                raise HTTPException(400, "XLSX expected: provide ?format=xlsx and multipart file")
            content = await file.read()
            df = pd.read_excel(BytesIO(content), sheet_name="Questionnaire")
            return assess_dataframe(df)
        else:
            if payload is None:
                raise HTTPException(400, "JSON expected in body")
            return assess_json(payload.model_dump())
    except Exception as e:
        raise HTTPException(500, f"Assessment failed: {e}") from e

class ReportRequest(BaseModel):
    result: AssessmentResult
    company_name: str = "Sample Company"

@app.post("/report")
async def report(req: ReportRequest):
    try:
        pdf = render_pdf_bytes(req.result.model_dump(), company_name=req.company_name)
        docx = render_docx_bytes(req.result.model_dump(), company_name=req.company_name)
        return {
            "pdf_bytes": pdf.hex(),
            "docx_bytes": docx.hex(),
            "message": "Hex-encoded bytes returned; clients should decode and save."
        }
    except Exception as e:
        raise HTTPException(500, f"Report generation failed: {e}") from e

class ReportRequestFile(BaseModel):
    result: AssessmentResult
    company_name: str = "Sample Company"
    brand: dict | None = None

@app.post("/report/file")
async def report_file(req: ReportRequestFile):
    try:
        brand = req.brand or {"primary":"#16BAC5","accent":"#1A1D2E","logo_b64":None}
        pdf = render_pdf_bytes(req.result.model_dump(), company_name=req.company_name, brand=brand)
        return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={req.company_name.replace(' ','_')}_Assessment.pdf"})
    except Exception as e:
        raise HTTPException(500, f"Report generation failed: {e}") from e
