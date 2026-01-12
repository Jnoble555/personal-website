import pandas as pd
import sqlite3

print("🏀 Designing SQL Schema for Championship DNA Analysis\n")
print("="*60)

# Check what data we have
print("\n1. Team Comparison Data:")
team_comp = pd.read_csv('data/raw/team_comparison.csv')
print(f"   Rows: {len(team_comp)}")
print(f"   Columns: {list(team_comp.columns)}")
print("\n   Sample:")
print(team_comp[['Team_Name', 'Year', 'Wins', 'Losses', 'PTS', 'FG%']].to_string())

print("\n" + "="*60)
print("\n2. Player Stats (2024 Celtics):")
players = pd.read_csv('data/raw/celtics_2024_table_1.csv')
print(f"   Rows: {len(players)}")
print(f"   Key stats: Player, Age, G, MP, PTS, AST, TRB")

print("\n" + "="*60)
print("\n3. SQLite Database (2012-2023 games):")
conn = sqlite3.connect('data/raw/nba.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]
print(f"   Tables: {tables}")
conn.close()

print("\n" + "="*60)
print("\nRECOMMENDED DATABASE STRUCTURE:")
print("="*60)

schema = """
TABLE: championship_teams
- team_id (PRIMARY KEY)
- team_name (e.g., '2024 Celtics')
- year
- wins
- losses
- win_pct
- points_per_game
- field_goal_pct
- three_point_pct
- rebounds_per_game
- assists_per_game
- steals_per_game
- blocks_per_game
- turnovers_per_game

TABLE: team_players (roster for each championship team)
- player_id (PRIMARY KEY)
- team_id (FOREIGN KEY)
- player_name
- age
- position
- games_played
- minutes_per_game
- points_per_game
- rebounds_per_game
- assists_per_game

TABLE: historical_games (from SQLite database)
- Already exists with game-by-game data
"""

print(schema)

print("\n✓ Ready to create the database!")
print("\nNext step: Run create_database.py")
