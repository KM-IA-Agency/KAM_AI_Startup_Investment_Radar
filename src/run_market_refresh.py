from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from src.load_to_db import load_seed_to_db


ROOT = Path(__file__).resolve().parents[1]


def run_command(command: list[str]) -> None:
    print("$ " + " ".join(command))
    result = subprocess.run(command, cwd=ROOT, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {' '.join(command)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a reusable market-analysis refresh cycle.")
    parser.add_argument(
        "--cadence",
        default="manual",
        choices=["manual", "daily", "every_2_days", "every_3_days", "weekly"],
        help="Refresh cadence label stored in analysis_runs.",
    )
    parser.add_argument(
        "--trigger-source",
        default="manual_cli",
        choices=["manual_cli", "cron", "github_actions", "streamlit_button", "external_scheduler"],
        help="Execution trigger stored in analysis_runs.",
    )
    parser.add_argument(
        "--skip-forecasting",
        action="store_true",
        help="Skip forecast generation and only load existing outputs/seeds into SQLite.",
    )
    parser.add_argument(
        "--no-reset",
        action="store_true",
        help="Append load instead of resetting seed-backed tables. Use carefully until upsert logic is implemented.",
    )
    args = parser.parse_args()

    if not args.skip_forecasting:
        run_command([sys.executable, "src/forecasting.py"])

    load_seed_to_db(
        reset=not args.no_reset,
        cadence=args.cadence,
        run_type="market_refresh",
        trigger_source=args.trigger_source,
    )

    print("Market refresh completed.")


if __name__ == "__main__":
    main()
