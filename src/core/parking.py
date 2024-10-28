from typing import Dict, List, Optional
from queue import PriorityQueue
from collections import deque
from .models import ParkingSpot

class ParkingLot:
    def __init__(self, is_multi_level: bool = False):
        self.is_multi_level = is_multi_level
        self.spots: Dict[str, ParkingSpot] = {}
        self.available_spots = PriorityQueue()
        self.levels: Dict[int, List[str]] = {}
        
    def add_parking_spot(self, spot_id: str, level: int, distance: float) -> None:
        spot = ParkingSpot(id=spot_id, level=level, distance_from_entrance=distance)
        self.spots[spot_id] = spot
        self.available_spots.put((distance, spot_id))
        
        if level not in self.levels:
            self.levels[level] = []
        self.levels[level].append(spot_id)

    def find_nearest_spot(self) -> Optional[str]: # use greedy algorithm
        if self.available_spots.empty():
            return None
            
        while not self.available_spots.empty():
            _, spot_id = self.available_spots.get()
            if not self.spots[spot_id].is_occupied:
                return spot_id
        return None

    def find_nearest_spot_bfs(self, start_level: int) -> Optional[str]: # only for multi-level parking!
        if not self.is_multi_level:
            return self.find_nearest_spot()
            
        visited_levels = set()
        queue = deque([start_level])
        
        while queue:
            current_level = queue.popleft()
            if current_level in visited_levels:
                continue
                
            visited_levels.add(current_level)
            
            for spot_id in self.levels.get(current_level, []):
                if not self.spots[spot_id].is_occupied:
                    return spot_id
            
            queue.extend([current_level - 1, current_level + 1])
        return None

    def allocate_spot(self, vehicle_id: str, spot_id: str) -> bool:
        if spot_id not in self.spots or self.spots[spot_id].is_occupied:
            return False
            
        spot = self.spots[spot_id]
        spot.is_occupied = True
        spot.vehicle_id = vehicle_id
        return True

    def release_spot(self, spot_id: str) -> bool:
        if spot_id not in self.spots or not self.spots[spot_id].is_occupied:
            return False
            
        spot = self.spots[spot_id]
        spot.is_occupied = False
        spot.vehicle_id = None
        self.available_spots.put((spot.distance_from_entrance, spot_id))
        return True