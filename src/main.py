from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from processor import EmailProcessor
from typing import Optional

app = FastAPI()
processor = EmailProcessor()

@app.get("/check-db")
async def check_db():
    tables = processor.db.verify_tables()
    accounts = processor.db.get_active_accounts()
    return {"tables": tables, "accounts": accounts}

@app.on_event("startup")
async def startup_event():
    processor.db.setup()

@app.get("/")
async def root():
    return {"message": "Email Processor API"}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    with open("dashboard.html") as f:
        return f.read()

@app.get("/search")
async def search(query: str):
    try:
        all_emails = await processor.get_all_emails()
        results = []
        for email in all_emails:
            if query.lower() in str(email).lower():
                results.append(email)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/process-emails")  # Remove trailing slash
async def process_recent_emails(limit: int = 10):
    try:
        results = await processor.process_new_emails(limit)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/add-email-account")
async def add_email_account(email: str, password: str, imap_server: str = "imap.gmail.com"):
    try:
        id = processor.db.add_email_account(email, password, imap_server)
        return {"status": "success", "id": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))