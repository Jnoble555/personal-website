import pandas as pd
import sqlite3

print("🏀 Creating Championship DNA Database\n")

# Connect to database (will create if doesn't exist)
conn = sqlite3.connect('data/processed/championship_dna.db')
cursor = conn.cursor()

print("Step 1: Creating championship_teams table...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS championship_teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    year INTEGER NOT NULL,
    wins INTEGER,
    losses INTEGER,
    win_pct REAL,
    points_per_game REAL,
    field_goal_pct REAL,
    three_point_pct REAL,
    rebounds_per_game REAL,
    assists_per_game REAL,
    steals_per_game REAL,
    blocks_per_game REAL,
    turnovers_per_game REAL
)
""")
print("✓ Table created")

print("\nStep 2: Loading team data...")
team_data = pd.read_csv('data/raw/team_comparison.csv')

# Clean and insert data
for _, row in team_data.iterrows():
    win_pct = row['Wins'] / (row['Wins'] + row['Losses'])
    
    cursor.execute("""
    INSERT INTO championship_teams (
        team_name, year, wins, losses, win_pct,
        points_per_game, field_goal_pct, three_point_pct,
        rebounds_per_game, assists_per_game, steals_per_game,
        blocks_per_game, turnovers_per_game
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['Team_Name'], row['Year'], row['Wins'], row['Losses'], win_pct,
        row['PTS'], row['FG%'], row['3P%'],
        row['TRB'], row['AST'], row['STL'],
        row['BLK'], row['TOV']
    ))

conn.commit()
print(f"✓ Inserted {len(team_data)} teams")

print("\nStep 3: Verifying data...")
result = pd.read_sql_query("SELECT * FROM championship_teams ORDER BY year DESC", conn)
print(result)

print("\nStep 4: Creating some sample queries...")

print("\n📊 Query 1: Teams ranked by winning percentage")
query1 = pd.read_sql_query("""
SELECT team_name, year, wins, losses, 
       ROUND(win_pct, 3) as win_percentage,
       ROUND(points_per_game, 1) as ppg
FROM championship_teams
ORDER BY win_pct DESC
""", conn)
print(query1)

print("\n📊 Query 2: Offensive comparison")
query2 = pd.read_sql_query("""
SELECT team_name, year,
       ROUND(points_per_game, 1) as ppg,
       ROUND(field_goal_pct, 3) as fg_pct,
       ROUND(three_point_pct, 3) as three_pct
FROM championship_teams
ORDER BY points_per_game DESC
""", conn)
print(query2)

conn.close()

print("\n✅ Database created successfully!")
print("📁 Location: data/processed/championship_dna.db")
print("\nYou can now run SQL queries on this database!")
