#!/usr/bin/env python
# -*- coding: utf-8 -*-#
from kivy.storage.jsonstore import JsonStore
import random
import string

make_lang_key = lambda s : filter(lambda x: x in string.printable, s)

class NameProvider(object):
    update_callback = None

    def __init__(self):
        self.name_store = JsonStore("names.json")
        self.rating_store = JsonStore("ratings.json")
        self.current_query = None
        self.cache = None

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
        try:
            return name, self.name_store.get(name)
        except KeyError:
            pass
        return None

    def _update_cache(self, gender, starts_with, ends_with, min_len, max_len, langs):
        self.cache = []

        for name, data in self.name_store.find():
            try:
                length = len(name)
                if length < int(min_len) or length > int(max_len):
                    continue
                if langs[make_lang_key(data["language"])]!=u'1':
                    continue
                if gender[0] in ("m", "w") and not data["gender"].startswith(gender[0]):
                    continue
                if starts_with != "" and not name.lower().startswith(starts_with):
                    continue
                if ends_with != "" and not name.lower().endswith(ends_with):
                    continue
                if self.rating_store.exists(name):
                    continue
                self.cache.append(name)
            except TypeError:
                pass

    def get_next_unrated_name(self, gender, starts_with, ends_with, min_len, max_len, langs):
        query = (gender, starts_with, ends_with, min_len, max_len, langs)

        if cmp(query, self.current_query) != 0:
            self._update_cache(*query)
            self.current_query = query

        if self.cache:
            next_name = random.choice(self.cache)
            self.cache.remove(next_name)

            return (next_name, self.get_by_name(next_name)), len(self.cache)

        return None, 0

    def rate(self, current_name, rating):
        self.rating_store.put(current_name[0], gender=current_name[1]["gender"], rating=rating)

    def get_favorites(self):
        return sorted([(x, y["gender"]) for x,y in self.rating_store.find(rating=1)])

    def delete_con_rating(self):
        cons = [x for x, _ in self.rating_store.find(rating=0)]

        for name in cons:
            self.rating_store.remove(name)

if __name__ == '__main__':
    name_prov = NameProvider()

    print name_prov.get_next_unrated_name()
