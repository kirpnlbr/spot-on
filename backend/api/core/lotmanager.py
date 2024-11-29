from typing import Dict
from .system import SpotOnSystem
from ..simulation.engine import ParkingSimulation

class ParkingLotManager:
    def __init__(self):
        self.parking_lots: Dict[str, ParkingSimulation] = {}

    def add_parking_lot(self, lot_name: str, num_levels: int, is_multi_level: bool,
                       arrival_rate: float = 0.7, departure_rate: float = 0.3):
        if lot_name not in self.parking_lots:
            simulation = ParkingSimulation(lot_name, num_levels, is_multi_level,
                                          arrival_rate=arrival_rate,
                                          departure_rate=departure_rate)
            self.parking_lots[lot_name] = simulation

    def get_parking_lot(self, lot_name: str) -> ParkingSimulation:
        return self.parking_lots.get(lot_name)

    def start_simulation(self, lot_name: str, duration_seconds: int = 60, update_interval: float = 2.0):
        simulation = self.get_parking_lot(lot_name)
        if simulation:
            simulation.start_simulation(duration_seconds, update_interval)

    def stop_simulation(self, lot_name: str):
        simulation = self.get_parking_lot(lot_name)
        if simulation:
            simulation.stop_simulation()

    def is_simulation_running(self, lot_name: str) -> bool:
        simulation = self.get_parking_lot(lot_name)
        return simulation.is_simulation_running if simulation else False