class ManualPriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, item):
        # Insert a new item into the priority queue.
        if item[0] is None:
            raise ValueError(f"Cannot push item with None priority: {item}")
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        # Remove and return the smallest item from the priority queue.
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        # Swap the first item with the last and remove the last (smallest)
        self._swap(0, -1)
        item = self.heap.pop()
        self._heapify_down(0)
        return item

    def is_empty(self):
        # Check if the priority queue is empty.
        return len(self.heap) == 0

    def remove(self, item):
        # Remove a specific item from the priority queue.
        # Returns True if the item was found and removed, False otherwise.
        try:
            index = self.heap.index(item)
        except ValueError:
            return False  # Item not found

        last_item = self.heap.pop()
        if index < len(self.heap):
            self.heap[index] = last_item
            self._heapify_down(index)
            self._heapify_up(index)
        return True

    def _heapify_up(self, index):
        # Maintain the heap property by moving the item at index up.
        parent = (index - 1) // 2
        if parent >= 0 and self.heap[index][0] < self.heap[parent][0]:
            self._swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index):
        # Maintain the heap property by moving the item at index down.
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left

        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right

        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def _swap(self, i, j):
        # Swap two items in the heap.
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def copy(self):
        # Create a shallow copy of the priority queue.
        new_queue = ManualPriorityQueue()
        new_queue.heap = self.heap.copy()
        return new_queue
