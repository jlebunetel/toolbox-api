from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/api/v1/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/showmyip/")
async def showmyip(request: Request):
    ip = request.client.host
    return {"ip": ip}
