import pandas as pd

print("🏀 Getting Team Totals from Basketball-Reference\n")

# Let's manually specify which teams/years and look for the "Team/Opponent" stats table
teams = [
    ('BOS', 2024, '2024 Celtics', 64, 18),  # Wins, Losses (you can verify these)
    ('DEN', 2023, '2023 Nuggets', 53, 29),
    ('GSW', 2022, '2022 Warriors', 53, 29),
    ('MIL', 2021, '2021 Bucks', 46, 26),
    ('LAL', 2020, '2020 Lakers', 52, 19),
]

team_stats = []

for team_abbr, year, name, wins, losses in teams:
    print(f"Fetching {name}...")
    url = f"https://www.basketball-reference.com/teams/{team_abbr}/{year}.html"
    
    try:
        # Get ALL tables
        tables = pd.read_html(url)
        
        # Look for table with "Team" and "Opponent" rows (usually team stats summary)
        for table in tables:
            # Check if first column has "Team" or "Opponent"
            if len(table) >= 2:
                first_col = table.iloc[:, 1] if len(table.columns) > 1 else table.iloc[:, 0]
                if 'Team' in str(first_col.values) or 'Lg Rank' in str(table.columns):
                    print(f"  ✓ Found team summary")
                    print(f"    Columns: {list(table.columns)[:10]}...")
                    
                    # Extract team row
                    team_row = table[table.iloc[:, 1].str.contains('Team', na=False)]
                    if len(team_row) > 0:
                        team_row = team_row.iloc[0].to_dict()
                        team_row['Team_Name'] = name
                        team_row['Year'] = year
                        team_row['Wins'] = wins
                        team_row['Losses'] = losses
                        team_stats.append(team_row)
                    break
        
    except Exception as e:
        print(f"  ✗ Error: {e}")

if team_stats:
    df = pd.DataFrame(team_stats)
    df.to_csv('data/raw/team_comparison.csv', index=False)
    print(f"\n✓ Saved {len(team_stats)} team stats!")
    print(df)
else:
    print("\n✗ Couldn't find team summary stats")