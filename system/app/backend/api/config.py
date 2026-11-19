"""Settings from environment variables (prefix DF_). Nothing is read from files at import time."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

APP_DIR = Path(__file__).resolve().parents[1]            # .../system/app/backend
SYSTEM_DIR = Path(__file__).resolve().parents[3]         # .../system


class Settings(BaseSettings):
    # Environment variables only. No implicit `.env`: system/app/.env belongs to Docker Compose (container values such as
    # DF_TRUST_PROXY=true) and must not leak into a process started on the host from that directory (17 Nov 2026).
    model_config = SettingsConfigDict(env_prefix='DF_', env_file=None, extra='ignore')

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
    # plan-system 4.5: items of one job running at the same time (so one long scan cannot take every worker); jobs of at
    # most `small_job_items` items get priority 1 and are claimed before normal jobs
    job_max_running_items: int = 2
    small_job_items: int = 10
    worker_poll_seconds: float = 1.0
    embedded_worker: bool = False                        # run the job worker inside the API process (single command)
    # Effect model used when a request names none (plan 2.12). Empty/None: the registry default (is_default row).
    default_model_id: str | None = None
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
    # Prediction cache (plan-system 1.2): memory (default, bounded LRU per process) | disk (opt-in: keeps sequences on
    # disk, see INSTALL.md) | off. Only model scores are cached, never domain status, warnings or annotations.
    prediction_cache: Literal['off', 'memory', 'disk'] = 'memory'
    prediction_cache_max_entries: int = 512
    prediction_cache_dir: Path | None = None             # disk mode only; default <workspace_dir>/../prediction-cache
    # Admin page (plan-system 4.2): client networks allowed to read /v1/admin/*. Loopback by default; the Docker compose
    # file adds the private ranges its proxy uses (the web port itself is bound to 127.0.0.1).
    admin_allowed_networks: list[str] = Field(default_factory=lambda: ['127.0.0.0/8', '::1/128'])

    @field_validator('default_model_id', mode='before')
    @classmethod
    def _empty_is_none(cls, v: object) -> object:
        return None if isinstance(v, str) and not v.strip() else v
