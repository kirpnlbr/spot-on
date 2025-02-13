import time
import random
from memory_profiler import profile
from api.core.parking import ParkingLot
from typing import Tuple, List, Dict
import math

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
        self.test_sizes = [100, 500, 1000, 5000]
        self.entry_points = {
            "corner": (0, 0),
            "center": (25, 25),
            "edge": (50, 0)
        }

    def create_corridor_layout(self, size: int) -> List[Tuple[str, int, float, Tuple[int, int]]]:
        """Creates spots along corridors radiating from entry point."""
        spots = []
        corridors = [(1, 0), (0, 1), (1, 1)]  # Horizontal, Vertical, Diagonal
        spot_index = 0

        for dx, dy in corridors:
            spots_in_corridor = size // len(corridors)
            for i in range(spots_in_corridor):
                x = i * dx
                y = i * dy
                distance = math.sqrt(x * x + y * y)
                spots.append((f"S{spot_index}", 0, distance, (x, y)))
                spot_index += 1

        return spots

    def create_multi_level_layout(self, size: int, num_levels: int) -> List[Tuple[str, int, float, Tuple[int, int]]]:
        """Creates spots across multiple levels with corridors on each level."""
        spots = []
        spots_per_level = size // num_levels

        for level in range(num_levels):
            level_spots = self.create_corridor_layout(spots_per_level)
            spots.extend([(f"L{level}S{i}", level, d, coord)
                          for i, (_, _, d, coord) in enumerate(level_spots)])

        return spots

    def simulate_arrivals(self, lot: ParkingLot, num_operations: int, arrival_rate: float) -> None:
        """Simulate vehicle arrivals."""
        for _ in range(int(num_operations * arrival_rate)):
            spot_id = random.choice(list(lot.spots.keys()))
            spot = lot.spots.get(spot_id)
            if spot and not spot.is_occupied:
                spot.is_occupied = True

    def simulate_departures(self, lot: ParkingLot, num_operations: int, departure_rate: float) -> None:
        """Simulate vehicle departures."""
        occupied_spots = [spot_id for spot_id, spot in lot.spots.items() if spot.is_occupied]
        for _ in range(int(num_operations * departure_rate)):
            if occupied_spots:
                spot_id = random.choice(occupied_spots)
                spot = lot.spots.get(spot_id)
                if spot:
                    spot.is_occupied = False
                    occupied_spots.remove(spot_id)

    @measure_time
    def test_priority_queue_single_level(self, size: int, arrival_rate: float, departure_rate: float, num_operations: int) -> None:
        """Test PQ performance with corridor layout."""
        lot = ParkingLot(is_multi_level=False)
        lot.set_entry_point(0, self.entry_points["corner"])

        # Add spots in corridor pattern
        spots = self.create_corridor_layout(size)
        for spot_id, level, distance, coordinate in spots:
            lot.add_parking_spot(spot_id, level, distance, coordinate)

        # Simulate arrivals and departures
        self.simulate_arrivals(lot, num_operations, arrival_rate)
        self.simulate_departures(lot, num_operations, departure_rate)

        # Find nearest spot
        nearest_spot = lot.find_nearest_spot_priority_queue(0)
        print(f"PQ - Found nearest spot: {nearest_spot}")

    @measure_time
    @profile
    def test_bfs_multi_level(self, size: int, num_levels: int, arrival_rate: float, departure_rate: float, num_operations: int) -> None:
        """Test BFS performance with multi-level corridor layout."""
        lot = ParkingLot(is_multi_level=True)

        # Set entry points for each level
        for level in range(num_levels):
            lot.set_entry_point(level, self.entry_points["corner"])

        # Add spots across multiple levels
        spots = self.create_multi_level_layout(size, num_levels)
        for spot_id, level, distance, coordinate in spots:
            lot.add_parking_spot(spot_id, level, distance, coordinate)

        # Simulate arrivals and departures
        self.simulate_arrivals(lot, num_operations, arrival_rate)
        self.simulate_departures(lot, num_operations, departure_rate)

        # Test finding nearest spot on each level
        for level in range(num_levels):
            print(f"\nSearching on level {level}:")
            nearest_spot = lot.find_nearest_spot_bfs(level)
            print(f"BFS - Found nearest spot on level {level}: {nearest_spot}")

    def run_tests(self) -> None:
        print("\nTesting Single-Level Priority Queue Implementation:")
        print("=" * 50)

        arrival_rate = 0.7
        departure_rate = 0.3
        num_operations = 1000  # Total number of operations to simulate

        for size in self.test_sizes:
            print(f"\nTesting with {size} spots:")
            self.test_priority_queue_single_level(size, arrival_rate, departure_rate, num_operations)

        print("\nTesting Multi-Level BFS Implementation:")
        print("=" * 50)

        for size in self.test_sizes:
            print(f"\nTesting with {size} total spots:")
            self.test_bfs_multi_level(size, num_levels=3, arrival_rate=arrival_rate, departure_rate=departure_rate, num_operations=num_operations)

if __name__ == "__main__":
    tester = PerformanceTest()
    tester.run_tests()
