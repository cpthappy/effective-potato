#!/usr/bin/env python
# -*- coding: utf-8 -*-#
from kivy.storage.jsonstore import JsonStore
import string

make_lang_key = lambda s : filter(lambda x: x in string.printable, s)

class NameProvider(object):
    update_callback = None

    def __init__(self):
        self.name_store = None
        self.rating_store = None
        self.current_query = None
        self.cache = None
        self.index = 0

    def get_rst(self, name, name_data):
        text = "**Sprache**\n\n  %s\n\n" % name_data["language"]
        if name_data["meaning"] != "-":
            text += "**Bedeutung**\n\n  %s \n\n" % name_data["meaning"]
        if name_data["origin"] != "-":
            text += "**Herkunft**\n\n %s\n\n" % name_data["origin"]
        if name_data["words"] != "-":
            text += u"**Wörter**\n\n %s\n\n" % name_data["words"]
        variants = [x for x in name_data["variants"] if x != name]
        if variants:
            text += "**Varianten**\n\n %s\n\n" % ', '.join(variants)

        return text

    def get_by_name(self, name):
        if not self.name_store:
            self.name_store = JsonStore("names.json")
        try:
            return name, self.name_store.get(name)
        except KeyError:
            pass
        return None

    def _update_cache(self, gender, starts_with, ends_with, min_len, max_len, langs):
        self.cache = []
        self.index = 0

        if not self.rating_store:
            self.rating_store = JsonStore("ratings.json")

        add_to_cache = self.cache.append

        gender_letter = gender[0]
        has_gender = gender_letter in ("m", "w")
        rating_store_exists = self.rating_store.exists
        min_len = int(min_len)
        max_len = int(max_len)

        if not self.name_store:
            self.name_store = JsonStore("names.json")
        if not self.rating_store:
            self.rating_store = JsonStore("ratings.json")

        for name, data in self.name_store.find():
            try:
                if has_gender and not data["gender"].startswith(gender_letter):
                    continue
                if data["length"] < min_len or data["length"] > max_len:
                    continue
                if rating_store_exists(name):
                    continue
                if langs[make_lang_key(data["language"])]!=u'1':
                    continue
                name_lc = name.lower()
                if starts_with != "" and not name_lc.startswith(starts_with):
                    continue
                if ends_with != "" and not name_lc.endswith(ends_with):
                    continue

                add_to_cache(name)

            except TypeError:
                pass
            except KeyError:
                pass

    def get_next_unrated_name(self, gender, starts_with, ends_with, min_len, max_len, langs):
        query = (gender, starts_with, ends_with, min_len, max_len, langs)

        if cmp(query, self.current_query) != 0:
            self._update_cache(*query)
            self.current_query = query

        if self.cache:
            #next_name = random.choice(self.cache)
            next_name = self.cache[self.index]
            self.index = (self.index + 1) % len(self.cache)
            return self.get_by_name(next_name), len(self.cache)

        return None, 0

    def rate(self, current_name, rating):
        if not self.rating_store:
            self.rating_store = JsonStore("ratings.json")
        self.cache.remove(current_name[0])
        self.rating_store.put(current_name[0], gender=current_name[1]["gender"], rating=rating)

    def change_rating(self, name, gender, rating):
        if not self.rating_store:
            self.rating_store = JsonStore("ratings.json")
        self.rating_store.put(name, gender=gender, rating=rating)

    def get_favorites(self):
        if not self.rating_store:
            self.rating_store = JsonStore("ratings.json")
        return sorted([(x, y["gender"]) for x,y in self.rating_store.find(rating=1)])

    def delete_con_rating(self):
        if not self.rating_store:
            self.rating_store = JsonStore("ratings.json")
        cons = [x for x, _ in self.rating_store.find(rating=0)]

        for name in cons:
            self.rating_store.delete(name)

        self._update_cache(*self.current_query)

if __name__ == '__main__':
    name_prov = NameProvider()

    print name_prov.get_next_unrated_name()
