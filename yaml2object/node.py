class Node:
    def __init__(self):
        self._public_props = [name for name in dir(self) if not name.startswith('__')]

    def __iter__(self):
        for prop in self._public_props:
            yield prop

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, item):
        self.__setattr__(key, item)
