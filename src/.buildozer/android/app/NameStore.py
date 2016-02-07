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

    def get_favorites(self):
        favs = []

        for name, data in self.store.find():
            try:
                if data["rating"] == 1:
                    favs.append((name, data))
            except KeyError:
                pass
        return favs

    def set_rating(self, current_name, rating_value):
        self.store.put(current_name[0], rating=rating_value, **current_name[1])

    def delete_con_rating(self):
        cons = []

        for name, data in self.store.find():
            try:
                if data["rating"] == 0:
                    cons.append((name, data))
            except KeyError:
                pass
        for name, data in cons:
            del data["rating"]
            self.store.put(name, **data)

if __name__ == "__main__":
    name_store = NameStore()
    print name_store.get_unrated_entries()
    print name_store.get_entry_by_name("Fang")
