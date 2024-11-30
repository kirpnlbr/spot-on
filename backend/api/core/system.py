from typing import Dict, List, Tuple, Optional
from .parking import ParkingLot
from .models import ParkingSpot
from collections import deque

class SpotOnSystem:
    def __init__(self, is_multi_level: bool = False):
        self.parking_lot = ParkingLot(is_multi_level=is_multi_level)
        self.vehicle_to_spot: Dict[str, str] = {}
        self.simulation: Optional['ParkingSimulation'] = None  # Reference to ParkingSimulation

    def initialize_parking_lot(self, spots_config: List[Tuple[str, int, Optional[float], Tuple[int, int]]]) -> None:
        for spot_id, level, distance, coordinate in spots_config:
            self.parking_lot.add_parking_spot(spot_id, level, distance, coordinate)

    def reset_parking_lot(self):
        for spot in self.parking_lot.spots.values():
            spot.is_occupied = False
            spot.vehicle_id = None
        self.vehicle_to_spot.clear()

    def park_vehicle(self, vehicle_id: str, preferred_level: int = 0) -> Optional[str]:
        if vehicle_id in self.vehicle_to_spot:
            return None  # Vehicle already parked

        spot_id = self.find_nearest_spot(preferred_level)
        if spot_id and self.allocate_spot(vehicle_id, spot_id):
            self.vehicle_to_spot[vehicle_id] = spot_id
            return spot_id
        return None

    def remove_vehicle(self, vehicle_id: str) -> bool:
        if vehicle_id not in self.vehicle_to_spot:
            return False  # Vehicle not found

        spot_id = self.vehicle_to_spot[vehicle_id]
        if self.release_spot(spot_id):
            del self.vehicle_to_spot[vehicle_id]
            return True
        return False

    def get_spot_info(self, spot_id: str) -> Optional[ParkingSpot]:
        return self.parking_lot.spots.get(spot_id)

    def get_vehicle_location(self, vehicle_id: str) -> Optional[str]:
        return self.vehicle_to_spot.get(vehicle_id)

    def get_total_occupied_spots(self) -> int:
        return len(self.vehicle_to_spot)

    def find_nearest_spot_priority_queue(self, level: int) -> Optional[str]:
        """
        Find the nearest available spot using the manual priority queue for a specific level.
        """
        if level not in self.parking_lot.entry_points:
            print(f"No entry point set for level {level}.")
            return None

        temp_queue = self.parking_lot.available_spots.copy()
        while not temp_queue.is_empty():
            distance, spot_id = temp_queue.pop()
            spot = self.parking_lot.spots.get(spot_id)
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
        if level not in self.parking_lot.entry_points:
            print(f"No entry point set for level {level}.")
            return None

        entry_point = self.parking_lot.entry_points[level]
        visited = set()
        queue = deque()
        queue.append(entry_point)
        visited.add(entry_point)

        # Get the set of valid coordinates for spots on this level
        valid_coords = {
            coord for spot_id, coord in self.parking_lot.spot_coordinates.items()
            if self.parking_lot.spots[spot_id].level == level
        }

        # If the entry point is not in valid_coords, find the closest valid coordinate
        if entry_point not in valid_coords:
            # Find the closest valid coordinate to the entry point
            closest_coord = min(valid_coords, key=lambda c: self.calculate_distance(entry_point, c))
            entry_point = closest_coord
            queue.clear()
            queue.append(entry_point)
            visited.add(entry_point)

        while queue:
            current_point = queue.popleft()
            spot_id = self.parking_lot.coord_to_spot_id.get((level, current_point))
            if spot_id:
                spot = self.parking_lot.spots.get(spot_id)
                if spot and not spot.is_occupied and spot.level == level:
                    print(f"Nearest spot (BFS) for level {level}: {spot_id} at {current_point}")
                    return spot_id

            # Explore neighboring points within valid coordinates
            neighbors = self.get_neighbors(current_point)
            for neighbor in neighbors:
                if neighbor not in visited and neighbor in valid_coords:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    print(f"Adding neighbor to queue: {neighbor} on level {level}")

        print(f"No available spots found using BFS for level {level}.")
        return None


    def get_neighbors(self, point: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Get adjacent points (up, down, left, right) that are valid parking spot coordinates.
        """
        x, y = point
        potential_neighbors = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1)
        ]
        # Filter neighbors to only those that exist in spot_coordinates
        valid_neighbors = [
            neighbor for neighbor in potential_neighbors
            if neighbor in self.parking_lot.spot_coordinates.values()
        ]
        return valid_neighbors


    def calculate_distance(self, point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
        """
        Calculate Manhattan distance between two points.
        """
        if not isinstance(point1, tuple) or not isinstance(point2, tuple):
            print(f"Invalid points format: {point1}, {point2}. Expected tuples of two integers.")
            return float('inf')
        x1, y1 = point1
        x2, y2 = point2
        distance = abs(x2 - x1) + abs(y2 - y1)
        print(f"Calculated distance between {point1} and {point2}: {distance:.2f}")
        return distance

    def find_nearest_spot(self, level: int) -> Optional[str]:
        """
        Determine which algorithm to use based on parking lot type and find the nearest spot for a specific level.
        """
        if self.parking_lot.is_multi_level:
            return self.find_nearest_spot_bfs(level)
        else:
            return self.find_nearest_spot_priority_queue(level)

    def allocate_spot(self, vehicle_id: str, spot_id: str) -> bool:
        """
        Allocate a spot to a vehicle.
        """
        spot = self.parking_lot.spots.get(spot_id)
        if spot and not spot.is_occupied:
            spot.is_occupied = True
            spot.vehicle_id = vehicle_id
            self.vehicle_to_spot[vehicle_id] = spot_id
            # Remove the spot from available spots
            success = self.parking_lot.available_spots.remove((spot.distance_from_entrance, spot_id))
            if success:
                print(f"Spot {spot_id} allocated to vehicle {vehicle_id}.")
                return True
            else:
                print(f"Failed to remove spot {spot_id} from available spots during allocation.")
        print(f"Failed to allocate spot {spot_id} to vehicle {vehicle_id}.")
        return False

    def release_spot(self, spot_id: str) -> bool:
        """
        Release a spot from a vehicle.
        """
        spot = self.parking_lot.spots.get(spot_id)
        if spot and spot.is_occupied:
            vehicle_id = spot.vehicle_id
            spot.is_occupied = False
            spot.vehicle_id = None
            # Removed the line that deletes vehicle_id from self.vehicle_to_spot
            # self.vehicle_to_spot.pop(vehicle_id, None)
            distance = spot.distance_from_entrance
            if distance != float('inf'):
                self.parking_lot.available_spots.push((distance, spot_id))
                print(f"Spot {spot_id} has been released and is now available.")
            else:
                print(f"Spot {spot_id} has invalid distance and was not added back to available spots.")
            return True
        print(f"Failed to release spot {spot_id}. It may already be vacant.")
        return False
