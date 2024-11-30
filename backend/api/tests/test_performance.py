import time
import sys
from memory_profiler import profile
from api.core.parking import ParkingLot
from typing import Tuple

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper


class PerformanceTest:
    def __init__(self):
        self.test_sizes = [100, 500, 1000, 5000]  # Different dataset sizes

    @measure_time
    def test_nearest_spot_priority_queue(self, size: int, level: int) -> None:
        """
        Test performance of finding the nearest spot using a priority queue.
        """
        lot = ParkingLot(is_multi_level=True)
        lot.set_entry_point(level, (0, 0))

        # Add parking spots with increasing distances
        for i in range(size):
            coordinate = (i, i)  # Dummy coordinates
            lot.add_parking_spot(f"S{i}", level, float(i), coordinate)

        # Find nearest spot using priority queue
        nearest_spot = lot.find_nearest_spot_priority_queue(level)
        print(f"Nearest spot using priority queue: {nearest_spot}")

    @measure_time
    @profile  # For memory usage
    def test_nearest_spot_bfs(self, size: int, level: int) -> None:
        """
        Test performance of finding the nearest spot using BFS.
        """
        lot = ParkingLot(is_multi_level=True)
        lot.set_entry_point(level, (0, 0))

        # Add parking spots with increasing distances
        for i in range(size):
            coordinate = (i, i)  # Dummy coordinates
            lot.add_parking_spot(f"S{i}", level, float(i), coordinate)

        # Find nearest spot using BFS
        nearest_spot = lot.find_nearest_spot_bfs(level)
        print(f"Nearest spot using BFS: {nearest_spot}")

    def run_tests(self) -> None:
        print("\nTesting Performance:")
        print("===================")
        level = 0  # Testing on level 0 for simplicity

        for size in self.test_sizes:
            print(f"\nTesting with {size} spots:")
            print("-" * 20)
            self.test_nearest_spot_priority_queue(size, level)
            self.test_nearest_spot_bfs(size, level)


if __name__ == "__main__":
    tester = PerformanceTest()
    tester.run_tests()