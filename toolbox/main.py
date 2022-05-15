import json
import requests

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

from toolbox import settings
from toolbox.star import get_next_bus

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

    if token != settings.DDNS_TOKEN:
        raise HTTPException(status_code=403, detail="token not valid!")

    if not domain:
        raise HTTPException(status_code=422, detail="domain not valid!")

    if not record:
        raise HTTPException(status_code=422, detail="record not valid!")

    address = "https://api.alwaysdata.com/v1/record/{record}/".format(record=record)

    credentials = (
        "{apikey} account={account}".format(
            apikey=settings.APIKEY, account=settings.ACCOUNT
        ),
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


@app.get("/api/v1/lametric/debug/")
async def lametric_debug():
    """LaMetric debug frames"""

    # https://help.lametric.com/support/solutions/articles/6000225467-my-data-diy
    # https://developer.lametric.com/icons

    return {
        "frames": [
            {
                "text": "Pikachu",
                "icon": "5588",  # Pikachu
            }
        ]
    }


@app.get("/api/v1/lametric/bus/{idarret}/")
async def next_bus(
    idarret: str,
    limit: int = 3,
):
    """Displays bus information on LaMetric"""

    horaires = get_next_bus(idarret=idarret, limit=limit)

    frames = [
        {
            "text": "bus",
            "icon": "996",  # bus
        }
    ]

    if horaires:
        for horaire in horaires:
            frames.append(
                {
                    "text": " ".join([horaire.nomcourtligne, horaire.depart]),
                }
            )
    else:
        frames.append(
            {
                "text": "Pas d'information ...",
                "icon": "625",  # Question
            }
        )

    return {
        "frames": frames,
    }
