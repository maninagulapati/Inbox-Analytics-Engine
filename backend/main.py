from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import base64
from backend.parser import parse_excel_attachment
from backend.storage import save_dataframe

app = FastAPI()

@app.post("/inbound")
async def receive_email(request: Request):
    payload = await request.json()
    attachments = payload.get("Attachments", [])

    for attachment in attachments:
        if attachment["ContentType"] in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "text/csv"]:
            content = base64.b64decode(attachment["Content"])
            filename = attachment["Name"].split('.')[0]
            sheets = parse_excel_attachment(content, attachment["Name"])
            save_dataframe(sheets, filename)

    return JSONResponse(content={"status": "ok"})