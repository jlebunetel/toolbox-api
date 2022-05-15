import json
import requests

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

from toolbox.settings import ACCOUNT, APIKEY, DDNS_TOKEN

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    # alwaysdata add to headers X-Real-IP, which takes the value of the client’s IP
    # address, see: https://help.alwaysdata.com/en/sites/http-stack/
    x_real_ip: Optional[str] = Header(None),
):
    """Returns the homepage"""

    ip = x_real_ip if x_real_ip else request.client.host

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "ip": ip,
        },
    )


@app.get("/api/v1/")
async def root():
    """API Root"""

    return {
        "message": "Hello World",
    }


@app.get("/api/v1/showmyip/")
async def showmyip(
    request: Request,
    # alwaysdata add to headers X-Real-IP, which takes the value of the client’s IP
    # address, see: https://help.alwaysdata.com/en/sites/http-stack/
    x_real_ip: Optional[str] = Header(None),
):
    """Returns my IP address"""

    ip = x_real_ip if x_real_ip else request.client.host

    return {
        "ip": ip,
    }


@app.get("/api/v1/ddns/")
async def ddns(
    request: Request,
    # alwaysdata add to headers X-Real-IP, which takes the value of the client’s IP
    # address, see: https://help.alwaysdata.com/en/sites/http-stack/
    x_real_ip: Optional[str] = Header(None),
    domain: int = 0,
    record: int = 0,
    name: str = "home",
    ip: str = "",
    token: str = "",
):
    """Sets my DDNS"""

    # https://api.alwaysdata.com/v1/record/doc/
    # Synology requires that the response body contains the string "good"

    if token != DDNS_TOKEN:
        raise HTTPException(status_code=403, detail="token not valid!")

    if not domain:
        raise HTTPException(status_code=422, detail="domain not valid!")

    if not record:
        raise HTTPException(status_code=422, detail="record not valid!")

    address = "https://api.alwaysdata.com/v1/record/{record}/".format(record=record)

    credentials = (
        "{apikey} account={account}".format(apikey=APIKEY, account=ACCOUNT),
        "",
    )

    if not ip:
        if x_real_ip:
            ip = x_real_ip
        else:
            ip = request.client.host

    data = {
        "domain": str(domain),
        "type": "A",
        "name": name,
        "value": ip,
    }

    _ = requests.put(
        address,
        auth=credentials,
        data=json.dumps(data),
    )

    return {
        "name": name,
        "type": "A",
        "value": ip,
        "detail": "good",
    }


@app.get("/api/v1/lametric/")
async def lametric():
    """LaMetric frames"""

    # https://help.lametric.com/support/solutions/articles/6000225467-my-data-diy

    return {
        "frames": [
            {
                "text": "LaMetric",
            }
        ]
    }
