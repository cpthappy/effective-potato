from kivy.storage.jsonstore import JsonStore

# (name, origin, gender, meaning, words, language))
store = JsonStore("src/names.json")

with open("data_det.txt", "r") as f:
    detailed = [x.strip().split('\t') for x in f.readlines()]

with open("data.txt", "r") as f:
    variants = [x.strip().split('\t') for x in f.readlines()]

print detailed[-1]

for entry in detailed:
    if store.exists(entry[0]):
        store.delete(entry[0])

    tmp_var = []
    for g,v,b in variants:
        if b == entry[0]:
            tmp_var.append(v)

    store.put(entry[0],
                gender=entry[2],
                language=entry[-1],
                variants = '\t'.join(tmp_var),
                words=entry[-2],
                origin=entry[1],
                meaning=entry[3])

# for key, entry in store.find():
#     print key, entry
