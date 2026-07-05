import os
import shutil

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.parser import parse_log
from app.services.summarizer import summarize_events
from app.services.gemini_service import analyze_security

from app.database import (
    create_database,
    save_report,
    get_reports,
)

from app.report_generator import generate_pdf

app = FastAPI(
    title="CyberGen AI",
    description="AI Powered Cybersecurity Incident Response Platform",
    version="2.0.0",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",
)

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)

# Create SQLite database automatically
create_database()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "CyberGen AI"
        },
    )


@app.post("/upload")
async def upload_log(
    request: Request,
    file: UploadFile = File(...),
):

    save_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse log
    events = parse_log(save_path)

    # Generate summary
    summary = summarize_events(events)

    # Risk Score
    risk_score = (
        summary["failed_login"] * 10
        + summary["sql_injection"] * 30
        + summary["xss"] * 25
        + summary["firewall"] * 15
        + summary["port_scan"] * 20
        + summary["malware"] * 40
    )

    risk_score = min(risk_score, 100)

    if risk_score < 25:
        risk = "LOW"
    elif risk_score < 50:
        risk = "MEDIUM"
    elif risk_score < 75:
        risk = "HIGH"
    else:
        risk = "CRITICAL"

    # AI Analysis
    ai_report = analyze_security(summary, events)

    # Suspicious IPs
    suspicious_ips = sorted(
        list(
            set(
                event["ip"]
                for event in events
                if event["ip"] != "Unknown"
            )
        )
    )

    # Save report to database
    save_report(
        file.filename,
        summary,
        risk,
        risk_score,
        ai_report,
    )

    # Generate PDF
    generate_pdf(
        file.filename,
        ai_report,
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "filename": file.filename,
            "events": events,
            "summary": summary,
            "risk": risk,
            "risk_score": risk_score,
            "ips": suspicious_ips,
            "ai_report": ai_report,
        },
    )


@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):

    reports = get_reports()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "reports": reports
        },
    )