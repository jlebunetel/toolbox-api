from fastapi import FastAPI, Request, Header
from typing import Optional

app = FastAPI()


@app.get("/api/v1/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/showmyip/")
async def showmyip(
    request: Request,
    user_agent: Optional[str] = Header(None),
    x_real_ip: Optional[str] = Header(None),
):
    ip = request.client.host
    return {
        "ip": ip,
        "headers": request["headers"],
        "User-Agent": user_agent,
        "X-Real-IP": x_real_ip,
    }
