import requests
import pandas as pd
import json
import os

employers = pd.read_csv("employers.csv")

employers = employers.dropna(subset=["url"])

print(employers)

results = {}

for _, row in employers.iterrows():
    try:
        response = requests.get(row["url"], timeout=10)

        results[row["company"]] = response.text

    except Exception as e:
        print(f"Error: {e}")

if os.path.exists("previous.json"):

    with open("previous.json") as f:
        previous = json.load(f)

else:
    previous = {}

changes = []

for company in results:

    old = previous.get(company, "")
    new = results[company]

    if old != new:
        changes.append(company)

print("\nChanges Detected:")

for company in changes:
    print(company)

with open("previous.json", "w") as f:
    json.dump(results, f)