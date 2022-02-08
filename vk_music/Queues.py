from queue import Queue


class Queues:
    def __init__(self):
        self.queues = {}

    def get(self, key):
        return self.queues.get(key)
