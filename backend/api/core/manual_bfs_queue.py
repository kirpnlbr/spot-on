class ManualBFSQueue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Add an item to the end of the queue."""
        self.items.append(item)

    def dequeue(self):
        """Remove and return the item from the front of the queue."""
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.items) == 0
