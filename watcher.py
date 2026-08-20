import requests
import pandas as pd
import json
import os
import smtplib
from email.message import EmailMessage

employers = pd.read_csv("employers.csv")

employers = employers.dropna(subset=["url"])

results = {}

for _, row in employers.iterrows():
    try:
        response = requests.get(row["url"], timeout=10)

        results[row["company"]] = response.text

    except Exception as e:
        print(f"Error: {e}")

with open("current.json", "w") as f:
    json.dump(results, f)

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

# SEND EMAIL IF CHANGES FOUND
if changes:

    email = os.environ["EMAIL_ADDRESS"]
    password = os.environ["EMAIL_PASSWORD"]

    msg = EmailMessage()

    msg["Subject"] = "Job Monitor Update"
    msg["From"] = email
    msg["To"] = email

    body = "Changes detected:\n\n"

    for company in changes:
        body += f"{company}\n"

    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(msg)

with open("previous.json", "w") as f:
    json.dump(results, f)