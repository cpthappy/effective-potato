from kivy.storage.jsonstore import JsonStore
from collections import Counter

TRESHOLD = 5


def format_lang(language):
    if language.startswith('Alt'):
        language = language.replace('Alt', '')
        language = language[0].upper() + language[1:]

    if language.startswith('Hochdeutsch'):
        return u'Deutsch'

    return language

# (name, origin, gender, meaning, words, language))
store = JsonStore("src/names.json")

with open("data_det.txt", "r") as f:
    detailed = [x.strip().split('\t') for x in f.readlines()]

with open("data.txt", "r") as f:
    variants = [x.strip().split('\t') for x in f.readlines()]

print detailed[-1]

langs = Counter()
names = []

for entry in detailed:
    if store.exists(entry[0]):
        store.delete(entry[0])

    tmp_var = []
    for g,v,b in variants:
        if b == entry[0]:
            tmp_var.append(v)

    language = format_lang(entry[-1])
    names.append((entry[0], language))
    store.put(entry[0],
                gender=entry[2],
                language=language,
                variants = tmp_var,
                words=entry[-2],
                origin=entry[1],
                meaning=entry[3])

    langs[language] += 1

print "Storing names complete. Filtering ..."
for key, lang in names:
    if langs[lang] < TRESHOLD:
        print key
        try:
            store.delete(key)
        except:
            print "XXX", key
print "...done"

for x, y in langs.iteritems():
    if y >= TRESHOLD:
        print repr(x)
