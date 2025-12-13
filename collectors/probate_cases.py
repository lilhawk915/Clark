"""Stub collector for Probate Court case planning.

Outputs a CSV plan for probate cases with unknown heirs. No scraping is
performed in this stub.
"""

import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List

CONFIG_PATH = Path("configs/clark_county_oh.json")
OUTPUT_PATH = Path("outputs/clark/probate/probate_plan.csv")
TARGET_IDS = {"probate_unknown_heir"}


def load_distress_config(config_path: Path = CONFIG_PATH) -> Dict:
    """Load the Clark County distress configuration JSON."""
    with config_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def select_probate_sources(distress_sources: Iterable[Dict]) -> List[Dict]:
    """Filter probate court distress sources."""
    return [source for source in distress_sources if source.get("id") in TARGET_IDS]


def write_probate_plan(sources: List[Dict], output_path: Path = OUTPUT_PATH) -> None:
    """Write a planning CSV for probate cases."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["id", "portal_url", "foia_needed", "notes"]

    with output_path.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for source in sources:
            writer.writerow(
                {
                    "id": source.get("id"),
                    "portal_url": source.get("portal_url"),
                    "foia_needed": bool(source.get("foia_needed")),
                    "notes": source.get("notes", ""),
                }
            )


def run() -> None:
    """Generate the probate case planning CSV."""
    config = load_distress_config()
    distress_sources = config.get("distress_sources", [])
    probate_sources = select_probate_sources(distress_sources)
    write_probate_plan(probate_sources)


if __name__ == "__main__":
    run()
