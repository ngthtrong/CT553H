"""API-50: property-based contract testing of every endpoint against system/openapi.yaml (schemathesis).

Positive and negative generation, in process (no network). Checks: no server error, every response status is one
listed for the operation in the contract, response bodies conform to the schema, error bodies are `Error`.
"""
from __future__ import annotations

import pytest
import schemathesis
from hypothesis import HealthCheck, settings
from schemathesis import checks as st_checks

from .conftest import mk_client
from .contract import check, spec

schema = schemathesis.openapi.from_dict(spec())


@schemathesis.check
def error_body_conforms(ctx, response, case):
    """Every error body is the `Error` schema (api-spec §5)."""
    if response.status_code >= 400:
        check('Error', response.json())


# status_code_conformance compares with the statuses listed for the operation in openapi.yaml, which the
# reconciliation of 22 Oct 2026 made complete (D-1..D-5 of DEVIATIONS.md).
CHECKS = [st_checks.not_a_server_error, st_checks.status_code_conformance, error_body_conforms,
          st_checks.response_schema_conformance]


@pytest.fixture(scope='module')
def contract_app(mini, mini_db, tmp_path_factory):
    import shutil
    path = tmp_path_factory.mktemp('c') / 'contract.db'
    shutil.copy(mini_db['path'], path)
    _, app = mk_client(mini, f'sqlite:///{path}')
    return app


@schema.parametrize()
@settings(max_examples=25, deadline=None, suppress_health_check=list(HealthCheck))
def test_api50_contract(case, contract_app):
    # `firstCells` in openapi.yaml is an excerpt (3 of 532 cells) and is not a response to validate
    case.call_and_validate(app=contract_app, checks=CHECKS)
