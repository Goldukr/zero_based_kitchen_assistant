import pandas as pd

item = input("Enter item name: ")
days = int(input("Enter expiry days: "))

new_data = {
    "item": item,
    "added_date": pd.Timestamp.today().strftime("%Y-%m-%d"),
    "expiry_days": days
}

df = pd.read_csv("inventory.csv")
df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
df.to_csv("inventory.csv", index=False)

print("Item added successfully!")
