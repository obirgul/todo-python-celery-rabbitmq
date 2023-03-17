import os
import time
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi import FastAPI

from src.settings import logger, config
from src import api_router

app = FastAPI(title="python-celery app", version=config.VERSION, description="Data Science Team - Hammer Bid Project")
app.include_router(api_router)


@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f}')
    return response


@app.get("/", include_in_schema=False)
async def main():
    return RedirectResponse(url="/docs/")


@app.get("/readiness", tags=['Info'])
async def readiness():
    logger.info("Readiness Success")
    return "OK"


@app.get("/info", tags=['Info'])
async def info():
    return {"VERSION": config.VERSION, "test": config.test, "git_commit_id": config.git_commit_id}


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", log_level="info", reload=True,  # workers=1,
                port=int(os.environ.get('uvicorn_port', 1234)))
