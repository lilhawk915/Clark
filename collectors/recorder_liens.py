"""Planning stub for Recorder lien collection tasks.

This module reads Clark County distress source configuration and writes a
CSV template for recorder lien targets. It does not fetch or scrape the
portal yet.
"""

import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List

CONFIG_PATH = Path("configs/clark_county_oh.json")
OUTPUT_PATH = Path("outputs/clark/recorder/liens_targets.csv")
RECORDER_IDS = {
    "mechanics_liens",
    "irs_state_tax_liens",
    "medicaid_liens",
    "child_support_judgment_liens",
}


def load_distress_config(config_path: Path = CONFIG_PATH) -> Dict:
    """Load the Clark County distress configuration JSON."""
    with config_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def select_recorder_sources(distress_sources: Iterable[Dict]) -> List[Dict]:
    """Filter distress sources for recorder lien work."""
    return [source for source in distress_sources if source.get("id") in RECORDER_IDS]


def write_recorder_targets(sources: List[Dict], output_path: Path = OUTPUT_PATH) -> None:
    """Write stub CSV rows for recorder lien collection."""
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
    """Generate the recorder lien target plan CSV."""
    config = load_distress_config()
    distress_sources = config.get("distress_sources", [])
    recorder_sources = select_recorder_sources(distress_sources)
    write_recorder_targets(recorder_sources)


if __name__ == "__main__":
    run()
