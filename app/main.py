from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.core import process_ticket

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_ticket(
    request: Request,
    message: str = Form(...),
    employee: str = Form(...)
):
    result, department = process_ticket(message, employee)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result_message": result,
        "department": department,
        "original_message": message
    })

if __name__ == "__main__":
    employee = input("Employee name: ")
    ticket = input("Submit your ticket: ")
    result, department = process_ticket(ticket, employee)
    print("\n✅ Result:", result)
    print("📂 Assigned department:", department)
