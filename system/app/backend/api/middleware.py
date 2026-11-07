"""Pure-ASGI middleware: request id, rate limit, security headers, and the privacy-safe access log.

The log line holds the method, the route *template* (never the concrete path or query), the status, the duration
and the request id. Sequences, accessions, tile numbers and share tokens never reach a log (NFR-09, NFR-19).
"""
from __future__ import annotations

import json
import logging
import time
import uuid

from starlette.types import ASGIApp, Message, Receive, Scope, Send

access_log = logging.getLogger('api.access')

SECURITY_HEADERS = [
    (b'x-content-type-options', b'nosniff'),
    (b'referrer-policy', b'no-referrer'),
]
API_CSP = (b'content-security-policy', b"default-src 'none'; frame-ancestors 'none'")
PREDICT_ROUTES = {('POST', '/v1/predict'), ('POST', '/v1/export'), ('POST', '/v1/runs')}


def _bucket(method: str, path: str) -> str | None:
    if path == '/healthz' or method == 'OPTIONS':
        return None
    if (method, path) in PREDICT_ROUTES:
        return 'predict'
    if path.startswith('/v1/'):
        return 'reference'
    return None


class CoreMiddleware:
    def __init__(self, app: ASGIApp, core) -> None:
        self.app = app
        self.core = core

    def _client(self, scope: Scope) -> str:
        if self.core.settings.trust_proxy:
            for k, v in scope.get('headers', []):
                if k == b'x-forwarded-for':
                    return v.decode('latin-1').split(',')[0].strip()
        client = scope.get('client')
        return client[0] if client else 'unknown'

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return
        request_id = uuid.uuid4().hex[:16]
        started = time.perf_counter()
        method, path = scope['method'], scope['path']
        status_holder = {'status': 500}
        api_path = path.startswith('/v1/') or path == '/healthz'

        async def send_wrapper(message: Message) -> None:
            if message['type'] == 'http.response.start':
                status_holder['status'] = message['status']
                headers = list(message.get('headers', []))
                headers.append((b'x-request-id', request_id.encode()))
                headers.extend(SECURITY_HEADERS)
                if api_path:
                    headers.append(API_CSP)
                message['headers'] = headers
            await send(message)

        bucket = _bucket(method, path)
        if bucket is not None:
            s = self.core.settings
            limit = s.rate_limit_predict if bucket == 'predict' else s.rate_limit_reference
            ok, retry = self.core.limiter.check(self._client(scope), bucket, limit)
            if not ok:
                body = json.dumps({'code': 'RATE_LIMITED', 'field': None,
                                   'message': f'Too many requests. Try again in {retry} seconds.'}).encode()
                await send_wrapper({'type': 'http.response.start', 'status': 429, 'headers': [
                    (b'content-type', b'application/json'), (b'content-length', str(len(body)).encode()),
                    (b'retry-after', str(retry).encode())]})
                await send_wrapper({'type': 'http.response.body', 'body': body})
                self._record(scope, method, 429, started, request_id)
                return
        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            self._record(scope, method, status_holder['status'], started, request_id)

    def _record(self, scope: Scope, method: str, status: int, started: float, request_id: str) -> None:
        route = scope.get('route')
        template = getattr(route, 'path', None) or ('/healthz' if scope['path'] == '/healthz' else '-')
        ms = (time.perf_counter() - started) * 1000
        access_log.info('%s %s %d %.1fms rid=%s', method, template, status, ms, request_id)
        model_id = (scope.get('state') or {}).get('model_id', '')
        self.core.usage.record(f'{method} {template}', model_id, status >= 400)
