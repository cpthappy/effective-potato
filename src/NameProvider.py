#!/usr/bin/env python
# -*- coding: utf-8 -*-#
from NameStore import NameStore
from ConfigStore import ConfigStore
import random

class NameProvider(object):
    update_callback = None

    def __init__(self):
        self.config_store = ConfigStore()
        self.name_store = NameStore()

    def get_next_unrated_name(self, gender, starts_with, ends_with, min_len, max_len):
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        print gender, starts_with, ends_with, min_len, repr(max_len)
        name_data = [x for x in self.name_store.get_unrated_entries()]
        print "LLLL", len(name_data)

        name_data = [x for x in name_data if len(x[0]) >= int(min_len) and len(x[0]) <= int(max_len)]
        print "LLLL2", len(name_data)

        if gender.startswith("j"):
            print "Geschlecht m gewaehlt"
            name_data = [x for x in name_data if x[1]["gender"] == "m"]
            print len(name_data)
        elif gender.startswith("m"):
            print "Geschlecht w gewählt"
            name_data = [x for x in name_data if x[1]["gender"] == "w"]
            print len(name_data)
        if starts_with != "":
            print "Anfang"
            name_data = [x for x in name_data if x[0].lower().startswith(starts_with)]
            print len(name_data)

        if ends_with != "":
            print "Ende"
            name_data = [x for x in name_data if x[0].lower().endswith(ends_with)]
            print len(name_data)

        print "YYYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

        if not name_data:
            return None

        return random.choice(name_data)

    def rate(self, current_name, rating):
        self.name_store.set_rating(current_name, rating)

    def get_favorites(self):
        return sorted(self.name_store.get_favorites())


if __name__ == '__main__':
    name_prov = NameProvider()

    print name_prov.get_next_unrated_name()
