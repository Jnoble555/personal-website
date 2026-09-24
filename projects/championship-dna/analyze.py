"""Run the portfolio's five-champion win-percentage comparison with SQLite."""

import csv
import sqlite3
from pathlib import Path


DATA = Path(__file__).with_name("champions_2020_2024.csv")
QUERY = """
SELECT team_name, year, wins, losses,
       ROUND(100.0 * wins / (wins + losses), 1) AS win_pct
FROM championship_teams
ORDER BY win_pct DESC, year DESC;
"""


def main() -> None:
    with DATA.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    with sqlite3.connect(":memory:") as db:
        db.execute(
            "CREATE TABLE championship_teams ("
            "team_name TEXT NOT NULL, year INTEGER NOT NULL, "
            "wins INTEGER NOT NULL, losses INTEGER NOT NULL)"
        )
        db.executemany(
            "INSERT INTO championship_teams VALUES (?, ?, ?, ?)",
            [
                (row["team_name"], int(row["year"]), int(row["wins"]), int(row["losses"]))
                for row in rows
            ],
        )
        for team, year, wins, losses, win_pct in db.execute(QUERY):
            print(f"{team:<16} {year}  {wins:>2}-{losses:<2}  {win_pct:>4.1f}%")


if __name__ == "__main__":
    main()
