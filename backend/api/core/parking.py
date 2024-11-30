from typing import Dict, List, Optional, Tuple
from .models import ParkingSpot
from .manual_priority_queue import ManualPriorityQueue
import math

class ParkingLot:
    def __init__(self, is_multi_level: bool = False):
        self.is_multi_level = is_multi_level
        self.spots: Dict[str, ParkingSpot] = {}
        self.available_spots: ManualPriorityQueue = ManualPriorityQueue()
        self.levels: Dict[int, List[str]] = {}
        self.entry_points: Dict[int, Tuple[int, int]] = {}  # Entry point per level
        self.vehicle_to_spot: Dict[str, str] = {}  # vehicle_id to spot_id
        self.spot_coordinates: Dict[str, Tuple[int, int]] = {}  # Map of spot_id to (x, y)
        self.coord_to_spot_id: Dict[Tuple[int, Tuple[int, int]], str] = {}  # Map of (level, coord) to spot_id


    def add_parking_spot(self, spot_id: str, level: int, distance: Optional[float], coordinate: Tuple[int, int]) -> None:
        if spot_id in self.spots:
            raise ValueError(f"Spot ID '{spot_id}' already exists.")

        if distance is None:
            distance = float('inf')  # Assign a default large distance if none is provided

        spot = ParkingSpot(id=spot_id, level=level, distance_from_entrance=distance)
        self.spots[spot_id] = spot
        self.spot_coordinates[spot_id] = coordinate
        self.coord_to_spot_id[(level, coordinate)] = spot_id

        if level not in self.levels:
            self.levels[level] = []
        self.levels[level].append(spot_id)

        # Only add to available_spots if the spot is not occupied and distance is valid
        if not spot.is_occupied and distance != float('inf'):
            self.available_spots.push((distance, spot_id))

    def set_entry_point(self, level: int, entry_point: Tuple[int, int]) -> None:
        self.entry_points[level] = entry_point



    def find_nearest_spot_priority_queue(self, level: int) -> Optional[str]:
        """
        Find the nearest available spot using the manual priority queue for a specific level.
        """
        if level not in self.entry_points:
            print(f"No entry point set for level {level}.")
            return None

        while not self.available_spots.is_empty():
            distance, spot_id = self.available_spots.pop()
            spot = self.spots.get(spot_id)
            if spot and not spot.is_occupied and spot.level == level:
                print(f"Nearest spot (Priority Queue) for level {level}: {spot_id} at distance {distance:.2f}")
                return spot_id
            else:
                print(f"Spot {spot_id} is occupied or not on level {level}. Continuing search.")
        print(f"No available spots found using Priority Queue for level {level}.")
        return None

    def find_nearest_spot_bfs(self, level: int) -> Optional[str]:
        """
        Find the nearest available spot using BFS for a specific level.
        """
        if level not in self.entry_points:
            print(f"No entry point set for level {level}.")
            return None

        entry_point = self.entry_points[level]
        visited = set()
        queue = deque()
        queue.append(entry_point)
        visited.add(entry_point)

        while queue:
            current_point = queue.popleft()
            print(f"BFS visiting point: {current_point} on level {level}")

            # Check if any spot exists at the current_point and is available
            for spot_id, coord in self.spot_coordinates.items():
                if coord == current_point:
                    spot = self.spots.get(spot_id)
                    if spot and not spot.is_occupied and spot.level == level:
                        print(f"Nearest spot (BFS) for level {level}: {spot_id} at {coord}")
                        return spot_id

            # Explore neighboring points
            neighbors = self.get_neighbors(current_point)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    print(f"Adding neighbor to queue: {neighbor} on level {level}")

        print(f"No available spots found using BFS for level {level}.")
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
