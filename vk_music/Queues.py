from queue import Queue


class Queues:
    def __init__(self):
        self.queues = {}
        self.sizes = {}
        self.looped = {}

    def add(self, key, func):
        if self.queues.get(key):
            self.queues[key].put(func)
        else:
            self.queues[key] = Queue()
            self.queues[key].put(func)
            self.looped[key] = False

    def is_looped(self, key):
        return self.looped.get(key, False)

    def set_loop(self, key, val):
        self.looped[key] = val

    def remove(self, key):
        if self.queues.get(key) is not None:
            del self.queues[key]

        if self.sizes.get(key) is not None:
            del self.sizes[key]

    def get(self, key):
        self.add_size(key, -1)
        if self.queues.get(key):
            return self.queues[key].get()
        return lambda: 0

    def add_size(self, key, size=1):
        self.sizes[key] = self.sizes.get(key, 0) + size
        return self.sizes[key]
