from typing import Dict, List, Optional, Tuple
from .models import ParkingSpot
from .manual_priority_queue import ManualPriorityQueue
from collections import deque
import math

class ParkingLot:
    def __init__(self, is_multi_level: bool = False):
        self.is_multi_level = is_multi_level
        self.spots: Dict[str, ParkingSpot] = {}
        self.available_spots: Dict[int, ManualPriorityQueue] = {}  # Priority queue per level
        self.levels: Dict[int, List[str]] = {}
        self.entry_points: Dict[int, Tuple[int, int]] = {}  # Entry point per level
        self.vehicle_to_spot: Dict[str, str] = {}  # vehicle_id to spot_id
        self.spot_coordinates: Dict[str, Tuple[int, int]] = {}  # Map of spot_id to (x, y)

    def add_parking_spot(self, spot_id: str, level: int, distance: float, coordinate: Tuple[int, int]) -> None:
        spot = ParkingSpot(id=spot_id, level=level, distance_from_entrance=distance)
        self.spots[spot_id] = spot
        self.spot_coordinates[spot_id] = coordinate

        if level not in self.available_spots:
            self.available_spots[level] = ManualPriorityQueue()
        self.available_spots[level].push((distance, spot_id))

        if level not in self.levels:
            self.levels[level] = []
        self.levels[level].append(spot_id)

    def set_entry_point(self, level: int, entry_point: Tuple[int, int]) -> None:
        self.entry_points[level] = entry_point

    def find_nearest_spot_priority_queue(self, level: int) -> Optional[str]:
        """
        Find the nearest available spot using the manual priority queue for a specific level.
        """
        if level not in self.entry_points:
            print(f"No entry point set for level {level + 1}.")
            return None

        if level not in self.available_spots:
            print(f"No available spots for level {level + 1}.")
            return None

        while not self.available_spots[level].is_empty():
            distance, spot_id = self.available_spots[level].peek()
            spot = self.spots.get(spot_id)
            if spot and not spot.is_occupied and spot.level == level:
                print(f"Nearest spot (Priority Queue) for level {level + 1}: {spot_id} at distance {distance:.2f}")
                return spot_id
            else:
                # Remove the spot from the queue if it's occupied or wrong level
                self.available_spots[level].pop()
                print(f"Spot {spot_id} is occupied or not on level {level + 1}. Continuing search.")
        print(f"No available spots found using Priority Queue for level {level + 1}.")
        return None

    def find_nearest_spot_bfs(self, level: int) -> Optional[str]:
        """
        Find the nearest available spot using BFS for a specific level.
        """
        if level not in self.entry_points:
            print(f"No entry point set for level {level + 1}.")
            return None

        entry_point = self.entry_points[level]
        visited = set()
        queue = deque()
        queue.append(entry_point)
        visited.add(entry_point)

        while queue:
            current_point = queue.popleft()
            print(f"BFS visiting point: {current_point} on level {level + 1}")

            # Check if any spot exists at the current_point and is available
            for spot_id, coord in self.spot_coordinates.items():
                if coord == current_point:
                    spot = self.spots.get(spot_id)
                    if spot and not spot.is_occupied and spot.level == level:
                        print(f"Nearest spot (BFS) for level {level + 1}: {spot_id} at {coord}")
                        return spot_id

            # Explore neighboring points
            neighbors = self.get_neighbors(current_point)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    print(f"Adding neighbor to queue: {neighbor} on level {level + 1}")

        print(f"No available spots found using BFS for level {level + 1}.")
        return None

    def get_neighbors(self, point: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Get adjacent points (up, down, left, right).
        """
        if not isinstance(point, tuple) or len(point) != 2:
            print(f"Invalid point format: {point}. Expected a tuple of two integers.")
            return []
        x, y = point
        neighbors = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1)
        ]
        return neighbors

    def calculate_distance(self, point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
        """
        Calculate Euclidean distance between two points.
        """
        if not isinstance(point1, tuple) or not isinstance(point2, tuple):
            print(f"Invalid points format: {point1}, {point2}. Expected tuples of two integers.")
            return float('inf')
        x1, y1 = point1
        x2, y2 = point2
        distance = math.hypot(x2 - x1, y2 - y1)
        print(f"Calculated distance between {point1} and {point2}: {distance:.2f}")
        return distance

    def find_nearest_spot(self, level: int) -> Optional[str]:
        """
        Use the appropriate method to find the nearest spot based on parking lot type.
        """
        if self.is_multi_level:
            return self.find_nearest_spot_bfs(level)
        else:
            return self.find_nearest_spot_priority_queue(level)

    def allocate_spot(self, vehicle_id: str, spot_id: str) -> bool:
        """
        Allocate a spot to a vehicle.
        """
        spot = self.spots.get(spot_id)
        if spot and not spot.is_occupied:
            spot.is_occupied = True
            spot.vehicle_id = vehicle_id
            self.vehicle_to_spot[vehicle_id] = spot_id
            print(f"Spot {spot_id} allocated to vehicle {vehicle_id}.")
            return True
        print(f"Failed to allocate spot {spot_id} to vehicle {vehicle_id}.")
        return False

    def release_spot(self, spot_id: str) -> bool:
        """
        Release a spot from a vehicle.
        """
        spot = self.spots.get(spot_id)
        if spot and spot.is_occupied:
            vehicle_id = spot.vehicle_id
            spot.is_occupied = False
            spot.vehicle_id = None
            self.vehicle_to_spot.pop(vehicle_id, None)
            distance = spot.distance_from_entrance
            level = spot.level
            if level not in self.available_spots:
                self.available_spots[level] = ManualPriorityQueue()
            self.available_spots[level].push((distance, spot_id))
            print(f"Spot {spot_id} has been released and is now available.")
            return True
        print(f"Failed to release spot {spot_id}. It may already be vacant.")
        return False
