import pandas as pd

# Load data
gdp = pd.read_csv("https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv")

# Search for Korea and Turkey variants
print("Searching for Korea variants:")
korea_matches = [c for c in gdp['Country Name'].unique() if 'korea' in c.lower()]
for country in korea_matches:
    print(f"  - {country}")

print("\nSearching for Turkey variants:")
turkey_matches = [c for c in gdp['Country Name'].unique() if 'turk' in c.lower()]
for country in turkey_matches:
    print(f"  - {country}")
