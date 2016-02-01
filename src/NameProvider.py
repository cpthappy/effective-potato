#!/usr/bin/env python
# -*- coding: utf-8 -*-#
from NameStore import NameStore
import random
import string

make_lang_key = lambda s : filter(lambda x: x in string.printable, s)

class NameProvider(object):
    update_callback = None

    def __init__(self):
        self.name_store = NameStore()

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
        return self.name_store.get_entry_by_name(name)

    def get_next_unrated_name(self, gender, starts_with, ends_with, min_len, max_len, langs):
        try:
            name_data = [x for x in self.name_store.get_unrated_entries() if langs[make_lang_key(x[1]["language"])]==u'1']
            name_data = [x for x in name_data if len(x[0]) >= int(min_len) and len(x[0]) <= int(max_len)]

            if gender.startswith("m"):
                name_data = [x for x in name_data if x[1]["gender"].startswith("m")]
            elif gender.startswith("w"):
                name_data = [x for x in name_data if x[1]["gender"].startswith("w")]

            if starts_with != "":
                name_data = [x for x in name_data if x[0].lower().startswith(starts_with)]

            if ends_with != "":
                name_data = [x for x in name_data if x[0].lower().endswith(ends_with)]
        except TypeError:
            return None, 0

        if not name_data:
            return None, 0

        return random.choice(name_data), len(name_data)

    def rate(self, current_name, rating):
        self.name_store.set_rating(current_name, rating)

    def get_favorites(self):
        return sorted(self.name_store.get_favorites())


if __name__ == '__main__':
    name_prov = NameProvider()

    print name_prov.get_next_unrated_name()
