import json
from typing import Optional

import requests
from fastapi import FastAPI, Header, HTTPException, Path, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from toolbox import settings
from toolbox.lametric import LaMetricFrame, LaMetricFrames
from toolbox.star import City, get_next_bus

app = FastAPI()

app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    """Returns the homepage"""

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Toolbox",
            "author": "Julien Lebunetel",
            "description": "A set of useful tools.",
            "author_twitter_id": "@jlebunetel",
            "site_url": "https://toolbox.blink-studio.com",
        },
    )


@app.get("/favicon.ico", response_class=FileResponse, include_in_schema=False)
async def get_favicon():
    return FileResponse(settings.FAVICON)


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

    if x_real_ip:
        return {"ip": x_real_ip}

    if request.client:
        return {"ip": request.client.host}

    return {"ip": ""}


@app.get("/api/v1/ddns/", include_in_schema=False)
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

    address = f"https://api.alwaysdata.com/v1/record/{record}/"

    credentials = (
        f"{settings.APIKEY} account={settings.ACCOUNT}",
        "",
    )

    if not ip:
        if x_real_ip:
            ip = x_real_ip
        elif request.client:
            ip = request.client.host
        else:
            ip = "0.0.0.0"

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
        timeout=1000,
    )

    return {
        "name": name,
        "type": "A",
        "value": ip,
        "detail": "good",
    }


@app.get(
    "/api/v1/lametric/debug/",
    response_model=LaMetricFrames,
    response_model_exclude_none=True,
)
async def lametric_debug() -> LaMetricFrames:
    """LaMetric debug frames"""

    return LaMetricFrames(
        frames=[
            LaMetricFrame(
                text="Pikachu",
                icon="5588",
            )
        ]
    )


@app.get(
    "/api/v1/lametric/cities/{city_id}/stops/{stop_id}/",
    response_model=LaMetricFrames,
    response_model_exclude_none=True,
)
async def lametric_next_bus(
    city_id: City,
    stop_id: str = Path(description="Timéo id", example="1056"),
    limit: int = 3,
) -> LaMetricFrames:
    """Displays bus information on LaMetric"""
    del city_id

    horaires = get_next_bus(idarret=stop_id, limit=limit)

    frames = LaMetricFrames(
        frames=[
            LaMetricFrame(
                text="bus",
                icon="996",
            )
        ],
    )

    if horaires:
        for horaire in horaires:
            frames.frames.append(
                LaMetricFrame(
                    text=" ".join([horaire.nomcourtligne, horaire.depart]),
                    icon="996",
                )
            )
    else:
        frames.frames.append(
            LaMetricFrame(
                text="Pas d'information ...",
                icon="625",  # Question
            )
        )

    return frames
