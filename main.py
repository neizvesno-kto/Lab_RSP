import time
from fastapi import FastAPI, Request
from logging_config import *

app = FastAPI()
logger = logging.getLogger("app")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"time={duration:.2f}ms"
    )

    return response

def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = (time.time() - start) * 1000

        logger.info(
            f"Method {func.__name__} executed in {duration:.2f}ms"
        )
        return result
    return wrapper


@log_execution_time
def process_data():
    time.sleep(0.5)

@app.get("/test")
def test():
    logger.info("Вызван тестовый endpoint")
    process_data()
    return {"status": "OK"}


@app.get("/error")
def error():
    try:
        1 / 0
    except Exception:
        logger.exception("Произошла ошибка")
        raise
