"""One error type for every rejected request; the API turns it into {code, message, field}."""
from __future__ import annotations


class DomainError(Exception):
    """A request that must be answered with a stable error code (see api-spec.md §5)."""

    def __init__(self, code: str, message: str, status: int, field: str | None = None,
                 dependencies: dict[str, int] | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.field = field
        self.dependencies = dependencies              # 409 CONFIRMATION_REQUIRED: counts, nothing deleted

    def body(self) -> dict:
        out: dict = {'code': self.code, 'message': self.message, 'field': self.field}
        if self.dependencies is not None:
            out['dependencies'] = self.dependencies
        return out
