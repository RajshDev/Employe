import logging
import time
import traceback
import uuid
from collections import defaultdict, deque
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("employee")


class AppError(Exception):
    status_code = 500
    message = "Something went wrong"

class EmployeeNotFoundError(AppError):
    status_code = 404
    message = "Employee not found"

class EmployeeAlreadyExistsError(AppError):
    status_code = 400
    message = "Employee already exists"


async def logging_and_error_middleware(request: Request, call_next):
    request_id = uuid.uuid4().hex[:8]
    start = time.time()
    try:
        response = await call_next(request)
    except AppError as exc:
        logger.warning(f"[{request_id}] {request.method} {request.url.path} -> {exc.status_code}: {exc.message}")
        response = JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": exc.message, "request_id": request_id},
        )
    except Exception as exc:
        tb = traceback.extract_tb(exc.__traceback__)
        own = [f for f in tb if "src/employee" in f.filename] or tb
        frame = own[-1]
        logger.error(
            f"[{request_id}] {request.method} {request.url.path} -> 500 | "
            f"{type(exc).__name__}: {exc} | file={frame.filename} line={frame.lineno} function={frame.name}"
        )
        response = JSONResponse(
            status_code=500,
            content={"success": False, "error": "Something went wrong", "request_id": request_id},
        )
    duration = (time.time() - start) * 1000
    logger.info(f"[{request_id}] {request.method} {request.url.path} -> {response.status_code} ({duration:.1f} ms)")
    response.headers["X-Request-ID"] = request_id
    return response


RATE_LIMIT = 3
WINDOW_SECONDS = 60
_hits: dict[str, deque] = defaultdict(deque)

async def rate_limit_middleware(request: Request, call_next):
    if request.method == "GET" and request.url.path.startswith("/employees"):
        client = request.client.host if request.client else "unknown"
        now = time.time()
        hits = _hits[client]
        while hits and now - hits[0] > WINDOW_SECONDS:
            hits.popleft()
        if len(hits) >= RATE_LIMIT:
            return JSONResponse(
                status_code=429,
                content={"success": False, "error": "Too many requests, try again after a minute"},
            )
        hits.append(now)
    return await call_next(request)