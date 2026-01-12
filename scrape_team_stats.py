import pandas as pd
import time

print("🏀 Scraping Team Stats for Championship Analysis\n")

# Teams we want: 2024 Celtics + recent champions
teams = [
    ('BOS', 2024, '2024 Celtics'),
    ('DEN', 2023, '2023 Nuggets'),
    ('GSW', 2022, '2022 Warriors'),
    ('MIL', 2021, '2021 Bucks'),
    ('LAL', 2020, '2020 Lakers'),
]

all_team_stats = []

for team_abbr, year, name in teams:
    print(f"Fetching {name}...")
    url = f"https://www.basketball-reference.com/teams/{team_abbr}/{year}.html"
    
    try:
        # Read the page - look for team totals table
        tables = pd.read_html(url)
        
        # Usually table with "Team" or "Opponent" in it
        for i, table in enumerate(tables):
            if 'Team' in table.columns or len(table.columns) > 20:
                print(f"  ✓ Found team stats table (index {i})")
                
                # Add team info
                table['Team'] = name
                table['Year'] = year
                table['Team_Abbr'] = team_abbr
                
                all_team_stats.append(table)
                break
        
        time.sleep(2)  # Be nice to the server
        
    except Exception as e:
        print(f"  ✗ Error: {e}")

if all_team_stats:
    # Combine all data
    df = pd.concat(all_team_stats, ignore_index=True)
    df.to_csv('data/raw/championship_teams_comparison.csv', index=False)
    print(f"\n✓ Saved data for {len(all_team_stats)} teams!")
    print(f"  File: data/raw/championship_teams_comparison.csv")
    print(f"\nPreview:")
    print(df.head())
else:
    print("\n✗ No data collected")
    