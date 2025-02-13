from .system import SpotOnSystem
from ..simulation.engine import ParkingSimulation

class ParkingLotManager:
    def __init__(self):
        self.parking_lots = {}

    def add_parking_lot(self, lot_name, num_levels, is_multi_level, address):
        if lot_name in self.parking_lots:
            raise ValueError(f"Parking lot '{lot_name}' already exists.")
        simulation = ParkingSimulation(lot_name, num_levels, is_multi_level, address)
        self.parking_lots[lot_name] = simulation

    def get_parking_lot(self, lot_name):
        return self.parking_lots.get(lot_name)

    def start_simulation(self, lot_name, duration_seconds, update_interval):
        simulation = self.get_parking_lot(lot_name)
        if simulation:
            simulation.start_simulation(duration_seconds, update_interval)
        else:
            raise ValueError(f"Parking lot '{lot_name}' not found.")

    def stop_simulation(self, lot_name):
        simulation = self.get_parking_lot(lot_name)
        if simulation:
            simulation.stop_simulation()
        else:
            raise ValueError(f"Parking lot '{lot_name}' not found.")

    def is_simulation_running(self, lot_name):
        simulation = self.get_parking_lot(lot_name)
        if simulation:
            return simulation.is_simulation_running
        else:
            return False
