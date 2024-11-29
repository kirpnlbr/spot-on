from typing import Dict, List, Optional, Tuple
from .parking import ParkingLot
from .models import ParkingSpot

class SpotOnSystem:
    def __init__(self, is_multi_level: bool = False):
        self.parking_lot = ParkingLot(is_multi_level)
        self.vehicle_to_spot: Dict[str, str] = {}

    def initialize_parking_lot(self, spots_config: List[Tuple[str, int, float]]) -> None: # spots_config: list of tuples containing (spot_id, level, distance)
        for spot_id, level, distance in spots_config:
            self.parking_lot.add_parking_spot(spot_id, level, distance)

    def reset_parking_lot(self):
        for spot in self.parking_lot.spots.values():
            spot.is_occupied = False
            spot.vehicle_id = None
        self.vehicle_to_spot.clear()

    def park_vehicle(self, vehicle_id: str, preferred_level: int = 0) -> Optional[str]:
        if vehicle_id in self.vehicle_to_spot: # note: should return allocated spot ID if successful and nothin if otherwise
            return None
            
        if self.parking_lot.is_multi_level:
            spot_id = self.parking_lot.find_nearest_spot_bfs(preferred_level)
        else:
            spot_id = self.parking_lot.find_nearest_spot()
            
        if spot_id and self.parking_lot.allocate_spot(vehicle_id, spot_id):
            self.vehicle_to_spot[vehicle_id] = spot_id
            return spot_id
        return None

    def remove_vehicle(self, vehicle_id: str) -> bool:
        if vehicle_id not in self.vehicle_to_spot:
            return False
            
        spot_id = self.vehicle_to_spot[vehicle_id]
        if self.parking_lot.release_spot(spot_id):
            del self.vehicle_to_spot[vehicle_id]
            return True
        return False

    def get_spot_info(self, spot_id: str) -> Optional[ParkingSpot]:
        return self.parking_lot.spots.get(spot_id)

    def get_vehicle_location(self, vehicle_id: str) -> Optional[str]:
        return self.vehicle_to_spot.get(vehicle_id)
    
    def get_total_occupied_spots(self) -> int:
        return len(self.vehicle_to_spot)