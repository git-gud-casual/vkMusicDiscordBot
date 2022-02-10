from queue import Queue


class Queues:
    def __init__(self):
        self.queues = {}
        self.playing = {}
        self.sizes = {}

    def add(self, key, func):
        if self.queues.get(key):
            self.queues[key].put(func)
        else:
            self.queues[key] = Queue()
            self.queues[key].put(func)

    def remove(self, key):
        if self.queues.get(key) is not None:
            del self.queues[key]

        if self.playing.get(key) is not None:
            del self.playing[key]

        if self.sizes.get(key) is not None:
            del self.sizes[key]

    def get(self, key):
        self.add_size(key, -1)
        if self.queues.get(key):
            return self.queues[key].get()
        self.set_playing(key, False)
        return lambda: 0

    def add_size(self, key, size=1):
        self.sizes[key] = self.sizes.get(key, 0) + size
        return self.sizes[key]

    def is_playing(self, key):
        return self.playing.get(key, False)

    def set_playing(self, key, val):
        self.playing[key] = val
