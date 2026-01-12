import pandas as pd

print("🏀 Scraping 2024 Celtics Championship Data...\n")

# URL for 2024 Celtics season
url = "https://www.basketball-reference.com/teams/BOS/2024.html"

try:
    # Read tables directly with pandas (includes User-Agent automatically)
    tables = pd.read_html(url)
    
    print(f"✓ Found {len(tables)} tables on the page\n")
    
    # Save each table
    for i, table in enumerate(tables):
        filename = f'data/raw/celtics_2024_table_{i}.csv'
        table.to_csv(filename, index=False)
        print(f"✓ Saved: {filename}")
        print(f"   Shape: {table.shape}")
        print(f"   Columns: {list(table.columns)[:5]}...\n")
    
    print("\n" + "="*60)
    print("SUCCESS! Data downloaded!")
    print("="*60)
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nBasketball-Reference might be blocking automated requests.")
    print("Let's try manually downloading the data instead...")