import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from automation_runner import run_automation
from config import OUTPUT_DIR

api = FastAPI(title="Revenue Report Automation API")


@api.get("/health")
def health_check():
    return {"status": "ok"}


@api.post("/run-automation")
def run_revenue_automation():
    try:
        result = run_automation()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api.get("/latest-pdf")
def get_latest_pdf():
    pdf_files = [
        os.path.join(OUTPUT_DIR, f)
        for f in os.listdir(OUTPUT_DIR)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        raise HTTPException(status_code=404, detail="No PDF found.")

    latest_pdf = max(pdf_files, key=os.path.getmtime)

    return FileResponse(
        latest_pdf,
        media_type="application/pdf",
        filename=os.path.basename(latest_pdf)
    )