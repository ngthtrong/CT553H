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
    gate_weights: Path | None = None                     # gate-weights.npz from experiment R3 (not available yet)
    gate_card: Path | None = None                        # gate-card.json
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
