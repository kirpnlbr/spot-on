import random
import threading
import time
from typing import Tuple, Optional
from datetime import datetime
from ..core.system import SpotOnSystem

class ParkingSimulation:
    def __init__(self, lot_name: str, num_levels: int, is_multi_level: bool,
                 arrival_rate: float = 0.7, departure_rate: float = 0.3):
        self.lot_name = lot_name
        self.is_multi_level = is_multi_level
        self.num_levels = num_levels
        self.level_layouts: Dict[int, Tuple[int, int]] = {}
        self.system = SpotOnSystem(is_multi_level=is_multi_level)
        self.total_spots: int = 0
        self.is_simulation_running: bool = False
        self.simulation_thread: Optional[threading.Thread] = None
        self.arrival_rate = arrival_rate
        self.departure_rate = departure_rate
        self.initialize_parking_lot()

    def initialize_parking_lot(self):
        self.total_spots = 0
        self.level_layouts = {}
        self.system.reset_parking_lot()  # Reset the parking lot

        for level in range(self.num_levels):
            # Randomly generate the number of rows and columns for this level (3-6)
            num_rows = random.randint(3, 6)
            num_cols = random.randint(3, 6)
            self.level_layouts[level] = (num_rows, num_cols)
            # Create slots for this level
            rows = [chr(ord('A') + i) for i in range(num_rows)]  # Generate row labels A-F
            spots_config = [
                (f"L{level+1}-{row}{col}", level, col * 2)
                for row in rows
                for col in range(1, num_cols + 1)
            ]
            # Initialize parking lot with this configuration
            self.system.initialize_parking_lot(spots_config)
            self.total_spots += len(spots_config)

        # Set target occupancy rate (e.g., 50% of spots occupied)
        target_occupancy_rate = 0.5
        spot_ids = list(self.system.parking_lot.spots.keys())

        # Shuffle the spot IDs for randomness
        random.shuffle(spot_ids)

        # Occupy 'spots_to_occupy' number of spots randomly from the shuffled list
        spots_to_occupy = int(len(spot_ids) * target_occupancy_rate)
        for spot_id in spot_ids[:spots_to_occupy]:
            vehicle_id = f"V{random.randint(1000, 9999)}"
            spot = self.system.parking_lot.spots[spot_id]
            spot.is_occupied = True
            spot.vehicle_id = vehicle_id
            self.system.vehicle_to_spot[vehicle_id] = spot_id

    def get_current_status(self) -> dict:
        total_occupied = sum(
            1 for spot in self.system.parking_lot.spots.values()
            if spot.is_occupied
        )

        # Serialize spots by level
        spots_by_level = {}
        for level in range(self.num_levels):
            spots_in_level = [
                {
                    "id": spot_id,
                    "isOccupied": spot.is_occupied,
                    "level": level + 1,  # Adjust level to be 1-based
                    "distance": spot.distance_from_entrance,
                    "vehicle_id": spot.vehicle_id,
                }
                for spot_id, spot in self.system.parking_lot.spots.items()
                if spot.level == level
            ]
            spots_by_level[level] = spots_in_level

        return {
            'timestamp': datetime.now(),
            'total_spots': self.total_spots,
            'occupied_spots': total_occupied,
            'available_spots': self.total_spots - total_occupied,
            'spots_by_level': spots_by_level,
            'level_layouts': self.level_layouts,
        }

    def simulate_vehicle_arrival(self) -> Tuple[str, bool]:
        vehicle_id = f"V{random.randint(1000, 9999)}"
        preferred_level = random.randint(0, self.num_levels - 1)
        spot_id = self.system.park_vehicle(vehicle_id, preferred_level)
        return vehicle_id, bool(spot_id)

    def simulate_vehicle_departure(self) -> bool:
        parked_vehicles = list(self.system.vehicle_to_spot.keys())
        if not parked_vehicles:
            return False
        vehicle_id = random.choice(parked_vehicles)
        return self.system.remove_vehicle(vehicle_id)

    def start_simulation(self, duration_seconds: int = 60, update_interval: float = 2.0):
        if self.is_simulation_running:
            return
        self.is_simulation_running = True
        self.simulation_thread = threading.Thread(target=self.run_simulation, args=(duration_seconds, update_interval))
        self.simulation_thread.start()

    def run_simulation(self, duration_seconds: int, update_interval: float):
        start_time = time.time()
        while self.is_simulation_running and (time.time() - start_time < duration_seconds):
            action = random.random()
            if action < self.arrival_rate:
                # Simulate vehicle arrival
                vehicle_id, success = self.simulate_vehicle_arrival()
                if success:
                    print(f"Vehicle {vehicle_id} parked successfully.")
                else:
                    print(f"Vehicle {vehicle_id} failed to park. No available spots.")
            elif action < self.arrival_rate + self.departure_rate:
                # Simulate vehicle departure
                success = self.simulate_vehicle_departure()
                if success:
                    print("A vehicle has left the parking lot.")
                else:
                    print("No vehicles to remove.")
            else:
                # Idle step (no action)
                print("No action this interval.")
            time.sleep(update_interval)
        self.is_simulation_running = False

    def stop_simulation(self):
        self.is_simulation_running = False
        if self.simulation_thread:
            self.simulation_thread.join()
            self.simulation_thread = None
