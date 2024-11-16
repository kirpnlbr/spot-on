from typing import Dict
from .system import SpotOnSystem
from ..simulation.engine import ParkingSimulation

class ParkingLotManager:
    def __init__(self):
        self.parking_lots: Dict[str, ParkingSimulation] = {}

    def add_parking_lot(self, lot_name: str, num_levels: int, is_multi_level: bool):
        if lot_name not in self.parking_lots:
            simulation = ParkingSimulation(lot_name, num_levels, is_multi_level)
            self.parking_lots[lot_name] = simulation

    def get_parking_lot(self, lot_name: str) -> ParkingSimulation:
        return self.parking_lots.get(lot_name)
