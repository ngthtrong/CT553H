"""Thin Python client of the local Degron Footprint API (plan-system 3.4). Standard library only.

    from api.client import Client
    c = Client('http://127.0.0.1:8080')
    r = c.predict(sequence='DIMFLVDSSGSIGPENFSKMKTFMKNLV')        # PredictionResult with provenance

Sequences travel only in request bodies, never in URLs (NFR-09). The client sends no Origin header, so the API's
cross-site write check (SEC-03) does not apply to it; it is meant for scripts on the same computer.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str, field: str | None = None):
        super().__init__(f'{status} {code}: {message}')
        self.status, self.code, self.message, self.field = status, code, message, field


class Client:
    def __init__(self, base_url: str = 'http://127.0.0.1:8080', timeout: float = 600.0):
        self.base = base_url.rstrip('/')
        self.timeout = timeout

    # ------------------------------------------------------------------ transport
    def _call(self, method: str, path: str, body: Any = None, raw: bool = False) -> Any:
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(self.base + path, data=data, method=method,
                                     headers={'Content-Type': 'application/json'} if data is not None else {})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:          # noqa: S310 (local API URL)
                payload = resp.read()
        except urllib.error.HTTPError as exc:
            try:
                err = json.loads(exc.read() or b'{}')
            except ValueError:
                err = {}
            raise ApiError(exc.code, err.get('code', 'HTTP_ERROR'), err.get('message', str(exc)),
                           err.get('field')) from None
        if raw:
            return payload.decode()
        return json.loads(payload) if payload else None

    # ------------------------------------------------------------------ operations
    def health(self) -> dict:
        return self._call('GET', '/healthz')

    def models(self) -> list[dict]:
        return self._call('GET', '/v1/models')['items']

    def predict(self, *, sequence: str | None = None, uniprot_id: str | None = None, tile_index: int | None = None,
                model_id: str | None = None, calibrator: str | None = None, override_domain: bool = False) -> dict:
        return self._call('POST', '/v1/predict', _tile_request(sequence, uniprot_id, tile_index, model_id, calibrator,
                                                                override_domain))

    def export(self, fmt: str = 'csv', **tile: Any) -> str:
        body = {**_tile_request(tile.get('sequence'), tile.get('uniprot_id'), tile.get('tile_index'),
                                tile.get('model_id'), tile.get('calibrator'), tile.get('override_domain', False)),
                'format': fmt}
        return self._call('POST', '/v1/export', body, raw=True)

    def create_project(self, name: str, description: str = '') -> dict:
        return self._call('POST', '/v1/projects', {'name': name, 'description': description})

    def save_analysis(self, project_id: str, **tile: Any) -> dict:
        req = _tile_request(tile.get('sequence'), tile.get('uniprot_id'), tile.get('tile_index'), tile.get('model_id'),
                            tile.get('calibrator'), tile.get('override_domain', False))
        return self._call('POST', f'/v1/projects/{_q(project_id)}/analyses', {'request': req})

    def submit_job(self, project_id: str, body: dict) -> dict:
        return self._call('POST', f'/v1/projects/{_q(project_id)}/jobs', body)

    def job(self, job_id: str) -> dict:
        return self._call('GET', f'/v1/jobs/{_q(job_id)}')

    def wait_job(self, job_id: str, poll: float = 2.0, timeout: float = 24 * 3600) -> dict:
        end = time.monotonic() + timeout
        while True:
            j = self.job(job_id)
            if j['state'] in ('completed', 'partial', 'failed', 'cancelled') or time.monotonic() > end:
                return j
            time.sleep(poll)

    def export_job(self, job_id: str, fmt: str = 'csv') -> str:
        return self._call('GET', f'/v1/jobs/{_q(job_id)}/export?format={_q(fmt)}', raw=True)

    def export_analysis(self, analysis_id: str, fmt: str = 'csv') -> str:
        return self._call('GET', f'/v1/analyses/{_q(analysis_id)}/export?format={_q(fmt)}', raw=True)

    def compare(self, analysis_a: str, analysis_b: str, save: bool = False) -> dict:
        return self._call('POST', '/v1/analyses/compare', {'analysis_a': analysis_a, 'analysis_b': analysis_b,
                                                            'save': save})


def _q(v: str) -> str:
    return urllib.parse.quote(str(v), safe='')


def _tile_request(sequence, uniprot_id, tile_index, model_id, calibrator, override_domain) -> dict:
    req: dict[str, Any] = {'sequence': sequence} if sequence is not None else {'uniprot_id': uniprot_id,
                                                                               'tile_index': tile_index}
    if model_id:
        req['model_id'] = model_id
    if calibrator:
        req['calibrator'] = calibrator
    if override_domain:
        req['override_domain'] = True
    return req


__all__ = ['Client', 'ApiError']
