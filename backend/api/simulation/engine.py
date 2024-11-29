import random
import threading
import time
import math
from typing import Tuple, Optional, Dict, List
from datetime import datetime
from ..core.system import SpotOnSystem
from ..core.manual_priority_queue import ManualPriorityQueue
import logging

# Configure logging
logger = logging.getLogger(__name__)

class ParkingSimulation:
    def __init__(
        self,
        lot_name: str,
        num_levels: int,
        is_multi_level: bool,
        occupancy_rate: float = 0.5  # Default occupancy rate of 50%
    ):
        self.lot_name = lot_name
        self.is_multi_level = is_multi_level
        self.num_levels = num_levels
        self.level_layouts: Dict[int, Tuple[int, int]] = {}
        self.system = SpotOnSystem(is_multi_level=is_multi_level)
        self.system.simulation = self  # Link SpotOnSystem back to this ParkingSimulation
        self.total_spots: int = 0
        self.is_simulation_running: bool = False
        self.simulation_thread: Optional[threading.Thread] = None
        self.occupancy_rate = occupancy_rate  # Initialize occupancy_rate
        self.perimeter_points: Dict[int, List[Tuple[int, int]]] = {}  # Entry points per level
        self.spot_coordinates: Dict[str, Tuple[int, int]] = {}  # Map of spot_id to (x, y)
        self.current_entry_points: Dict[int, Tuple[int, int]] = {}  # Current entry point per level
        self.nearest_spot_ids: Dict[int, Optional[str]] = {}  # Nearest spot ID per level
        self.initialize_parking_lot()
        self.set_initial_occupancy()  # Set initial occupancy after initialization

    def initialize_parking_lot(self):
        """
        Initialize the parking lot with spots, levels, and set initial occupancy.
        """
        logger.info(f"Initializing parking lot '{self.lot_name}' with {self.num_levels} levels.")
        self.total_spots = 0
        self.level_layouts = {}
        self.perimeter_points = {}
        self.spot_coordinates = {}
        self.system.parking_lot.spots.clear()  # Clear existing spots
        self.system.parking_lot.levels.clear()  # Clear existing levels
        self.system.parking_lot.available_spots = ManualPriorityQueue()  # Reset the manual priority queue
        self.system.parking_lot.vehicle_to_spot.clear()  # Clear any existing vehicle allocations
        self.current_entry_points = {}
        self.nearest_spot_ids = {}

        for level in range(self.num_levels):
            # Randomly generate the number of rows and columns for this level (3-6)
            num_rows = random.randint(4, 7)
            num_cols = random.randint(4, 7)
            self.level_layouts[level] = (num_rows, num_cols)
            logger.debug(f"Level {level + 1}: {num_rows} rows x {num_cols} columns.")

            # Create spots for this level
            rows = [chr(ord('A') + i) for i in range(num_rows)]  # Generate row labels A-F
            spots_config = [
                (f"L{level+1}-{row}{col}", level, col * 2, (col, i))
                for i, row in enumerate(rows)
                for col in range(1, num_cols + 1)
            ]

            # Initialize parking lot with this configuration
            for spot_id, lvl, distance, coord in spots_config:
                try:
                    self.system.parking_lot.add_parking_spot(spot_id, lvl, distance, coord)
                    self.spot_coordinates[spot_id] = coord  # Map spot_id to coordinates
                except ValueError as ve:
                    logger.error(str(ve))
                    continue  # Skip adding this spot if there's an error

            self.total_spots += len(spots_config)
            logger.info(f"Level {level + 1}: Added {len(spots_config)} spots.")

            # Define perimeter points (entry points) around the grid for this level
            perimeter = []
            for j in range(num_cols):
                # Top perimeter (y = -1)
                perimeter.append((j, -1))
                # Bottom perimeter (y = num_rows)
                perimeter.append((j, num_rows))
            for i in range(num_rows):
                # Left perimeter (x = -1)
                perimeter.append((-1, i))
                # Right perimeter (x = num_cols)
                perimeter.append((num_cols, i))
            self.perimeter_points[level] = perimeter

            # Set random entry point for this level
            if perimeter:
                random.shuffle(perimeter)
                entry_point = random.choice(perimeter)
                self.current_entry_points[level] = entry_point
                self.system.parking_lot.set_entry_point(level, entry_point)
                logger.info(f"Level {level + 1}: Initial Entry Point set to {entry_point}.")

                # Update distance_from_entry for each spot and populate available_spots priority queue
                for spot_id, _, _, _ in spots_config:
                    spot = self.system.parking_lot.spots.get(spot_id)
                    if spot:
                        distance = self.calculate_distance(entry_point, self.spot_coordinates[spot_id])
                        spot.distance_from_entrance = distance
                        # Update the priority queue with new distance
                        self.system.parking_lot.available_spots.push((distance, spot_id))
                    else:
                        logger.warning(f"Spot ID '{spot_id}' not found in spots dictionary.")

    def set_initial_occupancy(self):
        """
        Set the initial occupancy of parking spots based on occupancy_rate.
        """
        logger.info(f"Setting initial occupancy with rate {self.occupancy_rate * 100:.0f}%.")
        spot_ids = list(self.system.parking_lot.spots.keys())
        random.shuffle(spot_ids)
        spots_to_occupy = int(len(spot_ids) * self.occupancy_rate)
        occupied_spots = 0

        for spot_id in spot_ids[:spots_to_occupy]:
            spot = self.system.parking_lot.spots.get(spot_id)
            if spot and not spot.is_occupied:
                vehicle_id = f"V{random.randint(1000, 9999)}"
                success = self.system.allocate_spot(vehicle_id, spot_id)
                if success:
                    occupied_spots += 1
                    logger.info(f"Initially occupied spot {spot_id} by vehicle {vehicle_id}.")

        logger.info(f"Initial occupancy set: {occupied_spots} spots occupied.")

        # Update nearest spot for each level after initial occupancy
        for level in range(self.num_levels):
            self.update_nearest_spot(level)

    def update_nearest_spot(self, level: int):
        """
        Update the nearest available spot for a specific level.
        """
        logger.debug(f"Updating nearest spot for level {level + 1}.")
        nearest_spot_id = self.system.find_nearest_spot(level)
        self.nearest_spot_ids[level] = nearest_spot_id if nearest_spot_id else "N/A"
        if nearest_spot_id:
            logger.info(f"Nearest Spot Updated for level {level + 1}: {nearest_spot_id}")
        else:
            logger.info(f"No available nearest spot found for level {level + 1}.")

    def get_current_status(self) -> dict:
        """
        Retrieve the current status of the parking lot.
        """
        total_occupied = self.system.get_total_occupied_spots()
        logger.debug(f"Total occupied spots: {total_occupied}")

        # Serialize spots by level
        spots_by_level = {}
        for level in range(self.num_levels):
            spots_in_level = [
                {
                    "id": spot_id,
                    "isOccupied": spot.is_occupied,
                    "level": level + 1,  # Adjust level to be 1-based
                    "distance": self.system.calculate_distance(
                        self.current_entry_points.get(level),
                        self.spot_coordinates.get(spot_id, (0, 0))
                    ),
                    "vehicle_id": spot.vehicle_id,
                }
                for spot_id, spot in self.system.parking_lot.spots.items()
                if spot.level == level
            ]
            spots_by_level[level] = spots_in_level
            logger.debug(f"Level {level + 1}: {len(spots_in_level)} spots serialized.")

        status = {
            'timestamp': datetime.now().isoformat(),
            'total_spots': self.total_spots,
            'occupied_spots': total_occupied,
            'available_spots': self.total_spots - total_occupied,
            'spots_by_level': spots_by_level,
            'level_layouts': self.level_layouts,
            'nearest_spot_ids': self.nearest_spot_ids,  # Nearest spot per level
            'entry_points': self.current_entry_points,  # Entry point per level
        }
        logger.debug(f"Current status: {status}")
        return status

    def get_parking_grid(self, lot_name: str, level: int) -> Optional[dict]:
        """
        Retrieve the parking grid for a specific lot and level.
        """
        try:
            status_data = self.get_current_status()
            spots_by_level = status_data.get("spots_by_level", {})
            level_spots = spots_by_level.get(level, [])

            grid_data = {
                "lot_name": lot_name,
                "level": level + 1,  # Adjusting back to 1-based index for frontend
                "spots": level_spots,
                "level_layouts": self.level_layouts.get(level, ()),
                "nearest_spot_id": self.nearest_spot_ids.get(level, "N/A"),
                "entry_point": self.current_entry_points.get(level, "N/A"),
            }
            logger.debug(f"Retrieved grid data for lot '{lot_name}', level {level + 1}: {grid_data}")
            return grid_data
        except Exception as e:
            logger.exception(f"Error in get_parking_grid: {str(e)}")
            return None

    def simulate_vehicle_arrival(self) -> Tuple[str, bool, int]:
        """
        Simulate the arrival of a vehicle and attempt to park it.
        Returns a tuple of (vehicle_id, success, level).
        """
        vehicle_id = f"V{random.randint(1000, 9999)}"
        level = random.randint(0, self.num_levels - 1)
        entry_point = self.current_entry_points.get(level)

        if not entry_point:
            logger.error(f"No entry point set for level {level + 1}.")
            return vehicle_id, False, level + 1

        spot_id = self.system.find_nearest_spot(level)
        if spot_id:
            success = self.system.allocate_spot(vehicle_id, spot_id)
            if success:
                logger.info(f"Vehicle {vehicle_id} parked at {spot_id} on level {level + 1}.")
                # Update nearest spot after parking
                self.update_nearest_spot(level)
                return vehicle_id, True, level + 1
            else:
                logger.warning(f"Vehicle {vehicle_id} failed to park at {spot_id} on level {level + 1}.")
        else:
            logger.warning(f"Vehicle {vehicle_id} failed to park on level {level + 1}. No available spots.")
        return vehicle_id, False, level + 1

    def simulate_vehicle_departure(self) -> bool:
        """
        Simulate the departure of a random vehicle.
        Returns True if a vehicle was removed, False otherwise.
        """
        parked_vehicles = list(self.system.vehicle_to_spot.keys())
        if not parked_vehicles:
            logger.info("No vehicles to remove.")
            return False
        vehicle_id = random.choice(parked_vehicles)
        success = self.system.remove_vehicle(vehicle_id)
        if success:
            logger.info(f"Vehicle {vehicle_id} has left the parking lot.")
            # Retrieve the level from the spot to update the nearest spot
            spot_id = self.system.vehicle_to_spot.get(vehicle_id)
            if spot_id:
                spot = self.system.parking_lot.spots.get(spot_id)
                if spot:
                    level = spot.level
                    self.update_nearest_spot(level)
            return True
        else:
            logger.warning(f"Failed to remove vehicle {vehicle_id}.")
            return False

    def start_simulation(self, duration_seconds: int = 60, update_interval: float = 1.0, arrival_rate: float = 0.7, departure_rate: float = 0.3):
    
        if self.is_simulation_running:
            logger.warning("Simulation is already running.")
            return
        self.is_simulation_running = True
        self.simulation_thread = threading.Thread(target=self.run_simulation, args=(duration_seconds, update_interval, arrival_rate, departure_rate))
        self.simulation_thread.start()
        logger.info("Simulation started.")

    def run_simulation(self, duration_seconds: int, update_interval: float, arrival_rate: float, departure_rate: float):
        """
        Run the simulation loop, handling vehicle arrivals and departures.
        """
        start_time = time.time()
        logger.debug(f"Simulation running for {duration_seconds} seconds with update interval {update_interval} seconds.")
        while self.is_simulation_running and (time.time() - start_time < duration_seconds):
            action = random.random()
            if action < arrival_rate:
                # Simulate vehicle arrival
                vehicle_id, success, level = self.simulate_vehicle_arrival()
            elif action < arrival_rate + departure_rate:
                # Simulate vehicle departure
                self.simulate_vehicle_departure()
            else:
                # Idle step (no action)
                logger.debug("No action this interval.")
            time.sleep(update_interval)
        self.is_simulation_running = False
        logger.info("Simulation ended.")

    def stop_simulation(self):
        """
        Stop the simulation gracefully.
        """
        self.is_simulation_running = False
        if self.simulation_thread:
            self.simulation_thread.join()
            self.simulation_thread = None
        logger.info("Simulation stopped.")

    def calculate_distance(self, point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
        """
        Calculate Euclidean distance between two points.
        """
        if not isinstance(point1, tuple) or not isinstance(point2, tuple):
            logger.error(f"Invalid points format: {point1}, {point2}. Expected tuples of two integers.")
            return float('inf')
        x1, y1 = point1
        x2, y2 = point2
        distance = math.hypot(x2 - x1, y2 - y1)
        logger.debug(f"Calculated distance between {point1} and {point2}: {distance:.2f}")
        return distance
