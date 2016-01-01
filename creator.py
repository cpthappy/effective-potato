import csv
from kivy.storage.jsonstore import JsonStore

store = JsonStore("src/names.json")

with open("names_tab.csv", "r") as f:
    reader = csv.DictReader(f)

    for entry in reader:
        if store.exists(entry["Name"]):
            store.delete(entry["Name"])

        store.put(entry["Name"], gender=entry["Gender"], region=entry["Region"])

for key, entry in store.find():
    print key, entry
