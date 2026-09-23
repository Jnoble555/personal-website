"""Public excerpt of the local UltraTrain activity pipeline.

The example files are synthetic. This script keeps only run dates, distance,
and elapsed time; it never writes activity IDs, names, or route coordinates.
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import json
import math
from dataclasses import dataclass
from pathlib import Path

METERS_PER_MILE = 1609.344
STRAVA_DATE_FORMAT = "%b %d, %Y, %I:%M:%S %p"


@dataclass(frozen=True)
class Run:
    started: dt.datetime
    miles: float
    elapsed_minutes: float


def positive_number(value: str) -> float | None:
    """Reject blanks, text, non-finite values, and non-positive measurements."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) and number > 0 else None


def read_runs(path: Path) -> list[Run]:
    """Read the raw metric columns, which follow duplicate display columns."""
    runs = []
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source)
        header = next(reader)
        required = ("Activity Date", "Activity Type", "Distance", "Elapsed Time")
        missing = [name for name in required if name not in header]
        if missing:
            raise ValueError(f"Missing columns: {', '.join(missing)}")
        date_col = header.index("Activity Date")
        type_col = header.index("Activity Type")
        distance_col = max(i for i, name in enumerate(header) if name == "Distance")
        elapsed_col = max(i for i, name in enumerate(header) if name == "Elapsed Time")
        needed = max(date_col, type_col, distance_col, elapsed_col)

        for row in reader:
            if len(row) <= needed or row[type_col].strip() != "Run":
                continue
            meters = positive_number(row[distance_col])
            seconds = positive_number(row[elapsed_col])
            if meters is None or seconds is None:
                continue
            try:
                started = dt.datetime.strptime(row[date_col], STRAVA_DATE_FORMAT)
            except ValueError:
                continue
            runs.append(Run(started, meters / METERS_PER_MILE, seconds / 60))
    return sorted(runs, key=lambda run: run.started)


def monday(day: dt.date) -> dt.date:
    return day - dt.timedelta(days=day.weekday())


def weekly_training(runs: list[Run], race_date: dt.date) -> list[dict]:
    """Include empty weeks; exclude the milestone race from training volume."""
    training = [run for run in runs if run.started.date() < race_date]
    if not training:
        return []
    totals = collections.defaultdict(float)
    for run in training:
        totals[monday(run.started.date())] += run.miles

    week = monday(training[0].started.date())
    last_week = monday(race_date)
    weeks = []
    while week <= last_week:
        weeks.append({"week": week.isoformat(), "miles": round(totals[week], 1)})
        week += dt.timedelta(days=7)
    return weeks


def possible_overnight_matches(plan_path: Path | None, runs: list[Run]) -> list[str]:
    """Flag next-day runs before 4 a.m.; leave the intended match to a person."""
    if plan_path is None:
        return []
    with plan_path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        required = {"date", "planned_miles", "done"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Plan needs date, planned_miles, and done columns")
        flagged = []
        for row in reader:
            if row["done"].strip().lower() != "yes":
                continue
            if positive_number(row["planned_miles"]) is None:
                continue
            planned_date = dt.date.fromisoformat(row["date"])
            if any(run.started.date() == planned_date for run in runs):
                continue
            if any(
                run.started.date() == planned_date + dt.timedelta(days=1)
                and run.started.hour < 4
                for run in runs
            ):
                flagged.append(planned_date.isoformat())
        return flagged


def summarize(runs: list[Run], race_date: dt.date, plan_path: Path | None) -> dict:
    race_candidates = [run for run in runs if run.started.date() == race_date]
    if not race_candidates:
        raise ValueError(f"No run found on race date {race_date}")
    race = max(race_candidates, key=lambda run: run.miles)
    training = [run for run in runs if run.started.date() < race_date]
    return {
        "training_runs": len(training),
        "training_miles": round(sum(run.miles for run in training), 1),
        "race_miles": round(race.miles, 1),
        "weekly_training": weekly_training(runs, race_date),
        "possible_overnight_plan_matches": possible_overnight_matches(plan_path, runs),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("activities", type=Path, help="Strava-style activities.csv")
    parser.add_argument("--race-date", required=True, type=dt.date.fromisoformat)
    parser.add_argument("--plan", type=Path, help="Optional plan CSV")
    args = parser.parse_args()
    print(json.dumps(summarize(read_runs(args.activities), args.race_date, args.plan), indent=2))


if __name__ == "__main__":
    main()
