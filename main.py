from fastapi import FastAPI, Header, Request
from typing import Optional

app = FastAPI()


@app.get("/api/v1/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/showmyip/")
async def showmyip(
    request: Request,
    # alwaysdata add to headers X-Real-IP, which takes the value of the client’s IP
    # address, see: https://help.alwaysdata.com/en/sites/http-stack/
    x_real_ip: Optional[str] = Header(None),
):
    return {"ip": x_real_ip if x_real_ip else request.client.host}
