"""Error responses: every non-2xx body is {code, message, field}. Messages never contain stack traces or input."""
from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from degron_footprint.errors import DomainError

log = logging.getLogger('api.errors')


def error_response(status: int, code: str, message: str, field: str | None = None,
                   headers: dict[str, str] | None = None) -> JSONResponse:
    return JSONResponse({'code': code, 'message': message, 'field': field}, status_code=status, headers=headers)


def install(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def _domain(_: Request, exc: DomainError):
        return error_response(exc.status, exc.code, exc.message, exc.field)

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError):
        # FastAPI's own validation (path/query types). The offending value is never echoed.
        loc = [str(x) for x in exc.errors()[0].get('loc', ())] if exc.errors() else []
        field = loc[-1] if loc else None
        return error_response(422, 'INVALID_REQUEST', f'The request is invalid at "{field}".' if field
                              else 'The request is invalid.', field)

    @app.exception_handler(StarletteHTTPException)
    async def _http(_: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            return error_response(404, 'INVALID_REQUEST', 'No such route.')
        if exc.status_code == 405:
            return error_response(405, 'INVALID_REQUEST', 'Method not allowed for this route.')
        return error_response(exc.status_code, 'INVALID_REQUEST', 'The request cannot be served.')

    @app.exception_handler(SQLAlchemyError)
    async def _db(_: Request, exc: SQLAlchemyError):
        log.error('database error: %s', type(exc).__name__)       # class only: statements may hold input
        return error_response(503, 'SERVICE_UNAVAILABLE', 'The database is unavailable. Try again later.')

    @app.exception_handler(Exception)
    async def _unexpected(_: Request, exc: Exception):
        log.error('unexpected error: %s', type(exc).__name__)
        return error_response(500, 'INTERNAL_ERROR', 'Unexpected error. Quote the request id if you report it.')
