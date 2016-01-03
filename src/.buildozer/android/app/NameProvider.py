from NameStore import NameStore
from ConfigStore import ConfigStore
import random

class NameProvider(object):
    update_callback = None

    def __init__(self, callback=None):
        self.config_store = ConfigStore()
        self.name_store = NameStore()
        if callback is not None:
            NameProvider.update_callback = callback

    def get_next_unrated_name(self):

        name_data = self.name_store.get_unrated_entries()

        return random.choice(name_data)

    def rate(self, current_name, rating):
        self.name_store.set_rating(current_name, rating)

        print rating, NameProvider.update_callback
        if rating == 1 and NameProvider.update_callback:
            NameProvider.update_callback()

    def get_favorites(self):
        return sorted([x[0] for x in self.name_store.get_favorites()])


if __name__ == '__main__':
    name_prov = NameProvider()

    print name_prov.get_next_unrated_name()
