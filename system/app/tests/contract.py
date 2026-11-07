"""Validate response bodies against the schemas of system/openapi.yaml."""
from __future__ import annotations

import json
from functools import lru_cache

import yaml
from jsonschema import Draft202012Validator

from .conftest import CONTRACT


@lru_cache(maxsize=1)
def spec() -> dict:
    return json.loads(json.dumps(yaml.safe_load(CONTRACT.read_text()), default=str))


def validator(name: str) -> Draft202012Validator:
    return Draft202012Validator({'$ref': f'#/components/schemas/{name}', 'components': spec()['components']},
                                format_checker=Draft202012Validator.FORMAT_CHECKER)


def check(name: str, body) -> None:
    errors = sorted(validator(name).iter_errors(body), key=lambda e: list(e.path))
    assert not errors, f'{name}: ' + '; '.join(f"{list(e.path)}: {e.message}" for e in errors[:5])
