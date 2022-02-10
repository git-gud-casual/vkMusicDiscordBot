from queue import Queue


class Queues:
    def __init__(self):
        self.queues = {}
        self.playing = {}

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

    def size(self, key):
        if self.queues.get(key) is None:
            return 0
        return self.queues[key].qsize()

    def is_playing(self, key):
        return self.playing.get(key, False)

    def set_playing(self, key, val):
        self.playing[key] = val
