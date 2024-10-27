from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from queue import PriorityQueue
import heapq
from collections import deque

@dataclass
class ParkingSpot:
    id: str
    level: int
    distance_from_entrance: float
    is_occupied: bool = False
    vehicle_id: Optional[str] = None

class ParkingLot:
    def __init__(self, is_multi_level: bool = False):
        self.is_multi_level = is_multi_level
        self.spots: Dict[str, ParkingSpot] = {}  # Hash table for O(1) lookups
        self.available_spots = PriorityQueue()  # Min-heap for nearest spot allocation
        self.levels: Dict[int, List[str]] = {}  # For multi-level support
        
    def add_parking_spot(self, spot_id: str, level: int, distance: float) -> None:
        """Add a new parking spot to the system."""
        spot = ParkingSpot(id=spot_id, level=level, distance_from_entrance=distance)
        self.spots[spot_id] = spot
        
        # Add to priority queue with distance as priority
        self.available_spots.put((distance, spot_id))
        
        # Organize spots by level for multi-level support
        if level not in self.levels:
            self.levels[level] = []
        self.levels[level].append(spot_id)

    def find_nearest_spot(self) -> Optional[str]:
        """Find nearest available parking spot using greedy approach."""
        if self.available_spots.empty():
            return None
            
        # Keep checking until we find an actually available spot
        while not self.available_spots.empty():
            _, spot_id = self.available_spots.get()
            if not self.spots[spot_id].is_occupied:
                return spot_id
        return None

    def find_nearest_spot_bfs(self, start_level: int) -> Optional[str]:
        """Find nearest available spot using BFS for multi-level structures."""
        if not self.is_multi_level:
            return self.find_nearest_spot()
            
        # Use BFS to search levels starting from current level
        visited_levels = set()
        queue = deque([start_level])
        
        while queue:
            current_level = queue.popleft()
            if current_level in visited_levels:
                continue
                
            visited_levels.add(current_level)
            
            # Check spots in current level
            for spot_id in self.levels[current_level]:
                if not self.spots[spot_id].is_occupied:
                    return spot_id
            
            # Add adjacent levels to queue
            queue.extend([current_level - 1, current_level + 1])
            
        return None

    def allocate_spot(self, vehicle_id: str, spot_id: str) -> bool:
        """Allocate a specific spot to a vehicle."""
        if spot_id not in self.spots or self.spots[spot_id].is_occupied:
            return False
            
        spot = self.spots[spot_id]
        spot.is_occupied = True
        spot.vehicle_id = vehicle_id
        return True

    def release_spot(self, spot_id: str) -> bool:
        """Release a parking spot when vehicle leaves."""
        if spot_id not in self.spots or not self.spots[spot_id].is_occupied:
            return False
            
        spot = self.spots[spot_id]
        spot.is_occupied = False
        spot.vehicle_id = None
        
        # Re-add to available spots
        self.available_spots.put((spot.distance_from_entrance, spot_id))
        return True

class SpotOnSystem:
    def __init__(self, is_multi_level: bool = False):
        self.parking_lot = ParkingLot(is_multi_level)
        self.vehicle_to_spot: Dict[str, str] = {}  # Track vehicle locations

    def initialize_parking_lot(self, spots_config: List[Tuple[str, int, float]]) -> None:
        """Initialize parking lot with given configuration."""
        for spot_id, level, distance in spots_config:
            self.parking_lot.add_parking_spot(spot_id, level, distance)

    def park_vehicle(self, vehicle_id: str, preferred_level: int = 0) -> Optional[str]:
        """Park a vehicle in the nearest available spot."""
        if vehicle_id in self.vehicle_to_spot:
            return None  # Vehicle already parked
            
        if self.parking_lot.is_multi_level:
            spot_id = self.parking_lot.find_nearest_spot_bfs(preferred_level)
        else:
            spot_id = self.parking_lot.find_nearest_spot()
            
        if spot_id and self.parking_lot.allocate_spot(vehicle_id, spot_id):
            self.vehicle_to_spot[vehicle_id] = spot_id
            return spot_id
        return None

    def remove_vehicle(self, vehicle_id: str) -> bool:
        """Remove a vehicle from its parking spot."""
        if vehicle_id not in self.vehicle_to_spot:
            return False
            
        spot_id = self.vehicle_to_spot[vehicle_id]
        if self.parking_lot.release_spot(spot_id):
            del self.vehicle_to_spot[vehicle_id]
            return True
        return False

    def get_spot_info(self, spot_id: str) -> Optional[ParkingSpot]:
        """Get information about a specific parking spot."""
        return self.parking_lot.spots.get(spot_id)

    def get_vehicle_location(self, vehicle_id: str) -> Optional[str]:
        """Find where a vehicle is parked."""
        return self.vehicle_to_spot.get(vehicle_id)
    