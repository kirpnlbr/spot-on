import random
from typing import Tuple
from datetime import datetime
from ..core.system import SpotOnSystem

class ParkingSimulation:
    def __init__(self, num_levels: int, spots_per_level: int):
        self.system = SpotOnSystem(is_multi_level=num_levels > 1)
        self.num_levels = num_levels
        self.spots_per_level = spots_per_level
        self.total_spots = num_levels * spots_per_level
        self.initialize_parking_lot()
        
    def initialize_parking_lot(self):
        rows = ['A', 'B', 'C', 'D', 'E', 'F']
        spots_config = [
            (f"L{level+1}-{row}{col}", level, level * 10 + (col * 2))
            for level in range(self.num_levels)
            for row in rows
            for col in range(1, 6)
        ]
        
        self.system.initialize_parking_lot(spots_config)

    def simulate_vehicle_arrival(self) -> Tuple[str, bool]: # simulates a vehicle trying to park with its characteristics
        vehicle_id = f"V{random.randint(1000, 9999)}"
        preferred_level = random.randint(0, self.num_levels - 1)
        spot_id = self.system.park_vehicle(vehicle_id, preferred_level)
        return vehicle_id, bool(spot_id)

    def simulate_vehicle_departure(self) -> bool:
        parked_vehicles = list(self.system.vehicle_to_spot.keys()) # simulates a random parked vehicle leaving
        if not parked_vehicles:
            return False
        vehicle_id = random.choice(parked_vehicles)
        return self.system.remove_vehicle(vehicle_id)

    def get_current_status(self) -> dict: # occupancy status for visualization
        total_occupied = sum(
            1 for spot in self.system.parking_lot.spots.values()
            if spot.is_occupied
        )
        
        return {
            'timestamp': datetime.now(),
            'total_spots': self.total_spots,
            'occupied_spots': total_occupied,
            'available_spots': self.total_spots - total_occupied,
            'occupancy_rate': (total_occupied / self.total_spots) * 100,
            'spots_by_level': {
                level: [self.system.parking_lot.spots[spot_id] 
                       for spot_id in spots]
                for level, spots in self.system.parking_lot.levels.items()
            }
        }