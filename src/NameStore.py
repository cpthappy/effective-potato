from kivy.storage.jsonstore import JsonStore

class NameStore(object):

    def __init__(self):
        self.store = JsonStore("names.json")

    def get_entry_by_name(self, name):
        if self.store.exists(name):
            return name, self.store.get(name)

        return None

    def get_unrated_entries(self):
        unrated = []

        for name, data in self.store.find():
            if not "rating" in data.keys():
                unrated.append((name, data))
        return unrated

if __name__ == "__main__":
    name_store = NameStore()
    print name_store.get_unrated_entries()
    print name_store.get_entry_by_name("Fang")
