"""Settings from environment variables (prefix DF_). Nothing is read from files at import time."""
from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

APP_DIR = Path(__file__).resolve().parents[1]            # .../system/app/backend
SYSTEM_DIR = Path(__file__).resolve().parents[3]         # .../system


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DF_', env_file='.env', extra='ignore')

    database_url: str = 'sqlite:///./degron.db'
    model_dir: Path = APP_DIR / 'models'
    # Project-owned files (staged/committed imports). Copy together with the database for recovery (db-design §9).
    workspace_dir: Path = APP_DIR.parent / '.data' / 'workspace'
    # Workspace limits (proposed NFR-07 values; FR-36). JSON bodies of jobs/saves are larger than single predictions.
    max_workspace_body_bytes: int = 256 * 1024
    max_batch_peptides: int = 100
    max_protein_residues: int = 10_000
    max_import_bytes: int = 10 * 1024 * 1024
    max_import_rows: int = 100_000
    staged_import_hours: int = 24
    job_lease_seconds: int = 60
    worker_poll_seconds: float = 1.0
    embedded_worker: bool = False                        # run the job worker inside the API process (single command)
    gate_weights: Path | None = None                     # default: the file named in the gate card
    gate_card: Path | None = None                        # default: <model_dir>/gate.json written by the ETL (R3 gate)
    allowed_origins: list[str] = Field(default_factory=lambda: ['http://localhost:5173'])
    rate_limit_predict: int = 60                         # per client and window, prediction endpoints
    rate_limit_reference: int = 120                      # per client and window, reference endpoints
    rate_window_seconds: int = 60
    max_body_bytes: int = 4096
    share_ttl_default_days: int = 7
    share_ttl_max_days: int = 30
    trust_proxy: bool = False                            # read the client address from X-Forwarded-For
    enable_docs: bool = False
    openapi_contract: Path | None = SYSTEM_DIR / 'openapi.yaml'
    background_jobs: bool = True
    purge_interval_seconds: int = 3600
    usage_flush_seconds: int = 60
    log_level: str = 'INFO'
