from typing import Dict, Optional
from .system import SpotOnSystem
from ..simulation.engine import ParkingSimulation

class ParkingLotManager:
    def __init__(self):
        self.parking_lots: Dict[str, ParkingSimulation] = {}

    def add_parking_lot(self, lot_name: str, num_levels: int, is_multi_level: bool):
        if lot_name in self.parking_lots:
            raise ValueError(f"Parking lot '{lot_name}' already exists.")
        simulation = ParkingSimulation(lot_name, num_levels, is_multi_level)
        self.parking_lots[lot_name] = simulation

    def get_parking_lot(self, lot_name: str) -> Optional[ParkingSimulation]:
        return self.parking_lots.get(lot_name)

    def start_simulation(self, lot_name: str, duration_seconds: int, update_interval: float):
        simulation = self.get_parking_lot(lot_name)
        if simulation:
            simulation.start_simulation(duration_seconds, update_interval)
        else:
            raise ValueError(f"Parking lot '{lot_name}' not found.")

    def stop_simulation(self, lot_name: str):
        simulation = self.get_parking_lot(lot_name)
        if simulation:
            simulation.stop_simulation()
        else:
            raise ValueError(f"Parking lot '{lot_name}' not found.")

    def is_simulation_running(self, lot_name: str) -> bool:
        simulation = self.get_parking_lot(lot_name)
        if simulation:
            return simulation.is_simulation_running
        else:
            return False
