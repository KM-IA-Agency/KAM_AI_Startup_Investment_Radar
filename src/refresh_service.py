from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from src.load_to_db import load_seed_to_db


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class RefreshResult:
    status: str
    cadence: str
    trigger_source: str
    skip_forecasting: bool
    message: str


def _run_forecasting() -> None:
    command = [sys.executable, "src/forecasting.py"]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            "Forecast generation failed.\n"
            f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        )


def refresh_market_data(
    *,
    cadence: str = "manual",
    trigger_source: str = "streamlit_button",
    skip_forecasting: bool = False,
    reset: bool = True,
) -> RefreshResult:
    """Run an immediate market-data refresh and persist results in SQLite.

    This function is designed for Streamlit buttons and external schedulers.
    It does not directly clear Streamlit cache; the caller should do that after success.
    """
    if not skip_forecasting:
        _run_forecasting()

    load_seed_to_db(
        reset=reset,
        cadence=cadence,
        run_type="manual_market_refresh" if trigger_source == "streamlit_button" else "market_refresh",
        trigger_source=trigger_source,
    )

    return RefreshResult(
        status="success",
        cadence=cadence,
        trigger_source=trigger_source,
        skip_forecasting=skip_forecasting,
        message="Market data refreshed and written to SQLite.",
    )
