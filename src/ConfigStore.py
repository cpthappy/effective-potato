from kivy.storage.dictstore import DictStore

class ConfigStore(object):
    def __init__(self):
        self.store = DictStore("config.pkl")

    def get_gender_filter(self):
        if self.store.exists("gender_filter"):
            return self.store.get("gender_filter")
        else:
            return ""

    def set_gender_filter(self, value):
        self.store.put("gender_filter", value)

    def set_min_len_filter(self):
        pass

    def get_min_len_filter(self):
        pass

    def set_max_len_filter(self):
        pass

    def get_max_len_filter(self):
        pass

    def set_start_with_filter(self):
        pass

    def get_start_with_filter(self):
        pass
