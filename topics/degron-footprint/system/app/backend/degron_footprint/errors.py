"""One error type for every rejected request; the API turns it into {code, message, field}."""
from __future__ import annotations


class DomainError(Exception):
    """A request that must be answered with a stable error code (see api-spec.md §5)."""

    def __init__(self, code: str, message: str, status: int, field: str | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.field = field

    def body(self) -> dict:
        return {'code': self.code, 'message': self.message, 'field': self.field}
