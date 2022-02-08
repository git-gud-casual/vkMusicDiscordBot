class Queues:
    def __init__(self):
        self.queues = {}

    def get(self, key):
        if self.queues.get(key):
            return self.queues[key].pop(0)
        return None

    def add(self, key, name):
        if self.queues.get(key):
            self.queues[key].append(name)
        else:
            self.queues[key] = [name]
