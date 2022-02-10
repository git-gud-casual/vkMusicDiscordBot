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

    def get(self, key):
        self.set_playing(key, False)
        if self.queues.get(key):
            return lambda: self.queues[key].get()
        return lambda: 0

    def increment_size(self, key):
        val = self.sizes.get(key, 0)
        self.sizes[key] =  val + 1
        return val

    def is_playing(self, key):
        return self.playing.get(key, False)

    def set_playing(self, key, val):
        self.playing[key] = val
