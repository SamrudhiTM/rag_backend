import traceback
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.models.error_log import ErrorLog
from app.core.security import decode_access_token


async def get_user_id_from_request(request: Request) -> str | None:
    """Best-effort extraction of user id from the Authorization header, without raising."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ", 1)[1]
    payload = decode_access_token(token)
    if not payload:
        return None

    return payload.get("sub")


class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            user_id = await get_user_id_from_request(request)

            error_entry = ErrorLog(
                endpoint=str(request.url.path),
                method=request.method,
                error_message=str(exc),
                stack_trace=traceback.format_exc(),
                user_id=user_id,
            )
            await error_entry.insert()

            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error. Please try again later."},
            )