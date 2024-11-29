from typing import List, Tuple, Optional

class ManualPriorityQueue:
    def __init__(self):
        self.heap: List[Tuple[float, str]] = []

    def push(self, item: Tuple[float, str]) -> None:
        """
        Insert a new item into the priority queue.
        """
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def pop(self) -> Optional[Tuple[float, str]]:
        """
        Remove and return the smallest item from the priority queue.
        """
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        # Swap the first item with the last and remove the last (smallest)
        self._swap(0, -1)
        item = self.heap.pop()
        self._heapify_down(0)
        return item

    def peek(self) -> Optional[Tuple[float, str]]:
        """
        Return the smallest item from the priority queue without removing it.
        """
        if not self.heap:
            return None
        return self.heap[0]

    def is_empty(self) -> bool:
        """
        Check if the priority queue is empty.
        """
        return len(self.heap) == 0

    def _heapify_up(self, index: int) -> None:
        """
        Maintain the heap property by moving the item at index up.
        """
        parent = (index - 1) // 2
        if parent >= 0 and self.heap[index][0] < self.heap[parent][0]:
            self._swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index: int) -> None:
        """
        Maintain the heap property by moving the item at index down.
        """
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

    def _swap(self, i: int, j: int) -> None:
        """
        Swap two items in the heap.
        """
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
