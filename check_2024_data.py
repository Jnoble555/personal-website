import pandas as pd

print("🏀 Checking 2024 Celtics Data\n")

for i in range(5):
    print("="*60)
    print(f"Table {i}:")
    print("="*60)
    
    df = pd.read_csv(f'data/raw/celtics_2024_table_{i}.csv')
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}\n")
    print("First 3 rows:")
    print(df.head(3))
    print("\n")