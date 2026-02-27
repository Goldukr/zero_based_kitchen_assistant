import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv("inventory.csv")

today = datetime.today()

print("Items Expiring Soon:\n")

for index, row in df.iterrows():
    added_date = datetime.strptime(row["added_date"], "%Y-%m-%d")
    expiry_date = added_date + timedelta(days=row["expiry_days"])

    if (expiry_date - today).days <= 2 and (expiry_date - today).days >= 0:
        print(row["item"], "is expiring soon on", expiry_date.date())
