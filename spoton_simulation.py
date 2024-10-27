import time
import random
from typing import List, Tuple
import os
from datetime import datetime

# Import our main system
from spoton_implementation import SpotOnSystem, ParkingSpot

class ParkingSimulation:
    def __init__(self, num_levels: int, spots_per_level: int):
        self.system = SpotOnSystem(is_multi_level=num_levels > 1)
        self.num_levels = num_levels
        self.spots_per_level = spots_per_level
        self.total_spots = num_levels * spots_per_level
        self.initialize_parking_lot()
        
    def initialize_parking_lot(self):
        """Create parking spot configuration."""
        spots_config = []
        for level in range(self.num_levels):
            for spot in range(self.spots_per_level):
                spot_id = f"L{level+1}-S{spot+1}"
                # Distance increases with level and spot number
                distance = level * 10 + (spot * 2)
                spots_config.append((spot_id, level, distance))
        
        self.system.initialize_parking_lot(spots_config)
        
    def clear_screen(self):
        """Clear console screen for better visualization."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_parking_status(self):
        """Display current parking lot status."""
        self.clear_screen()
        print("\n=== SpotOn Parking System Status ===")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 40)
        
        total_occupied = 0
        for level in range(self.num_levels):
            print(f"\nLevel {level + 1}:")
            print("-" * 20)
            
            spots_in_level = [spot for spot_id, spot in self.system.parking_lot.spots.items() 
                            if spot.level == level]
            
            # Create visual representation
            for i in range(0, self.spots_per_level, 5):  # Show 5 spots per line
                line = ""
                for j in range(5):
                    if i + j < len(spots_in_level):
                        spot = spots_in_level[i + j]
                        if spot.is_occupied:
                            line += "[X] "
                            total_occupied += 1
                        else:
                            line += "[ ] "
                print(line)
                
        # Display statistics
        occupancy_rate = (total_occupied / self.total_spots) * 100
        print("\n=== Statistics ===")
        print(f"Total Spots: {self.total_spots}")
        print(f"Occupied Spots: {total_occupied}")
        print(f"Available Spots: {self.total_spots - total_occupied}")
        print(f"Occupancy Rate: {occupancy_rate:.1f}%")
        print("=" * 40)

    def simulate_vehicle_arrival(self) -> Tuple[str, bool]:
        """Simulate a vehicle arriving and trying to park."""
        vehicle_id = f"V{random.randint(1000, 9999)}"
        preferred_level = random.randint(0, self.num_levels - 1)
        
        spot_id = self.system.park_vehicle(vehicle_id, preferred_level)
        return vehicle_id, bool(spot_id)

    def simulate_vehicle_departure(self) -> bool:
        """Simulate a random parked vehicle leaving."""
        parked_vehicles = list(self.system.vehicle_to_spot.keys())
        if not parked_vehicles:
            return False
            
        vehicle_id = random.choice(parked_vehicles)
        return self.system.remove_vehicle(vehicle_id)

    def run_simulation(self, duration_seconds: int = 60, update_interval: float = 2.0):
        """Run the parking simulation for a specified duration."""
        print(f"\nStarting simulation for {duration_seconds} seconds...")
        print("Press Ctrl+C to stop the simulation")
        
        start_time = time.time()
        try:
            while time.time() - start_time < duration_seconds:
                # Randomly decide whether to simulate arrival or departure
                if random.random() < 0.7:  # 70% chance of arrival
                    vehicle_id, success = self.simulate_vehicle_arrival()
                    action = f"Vehicle {vehicle_id} arrived and {'found' if success else 'failed to find'} a spot"
                else:
                    success = self.simulate_vehicle_departure()
                    action = f"Vehicle departure was {'successful' if success else 'failed'}"
                
                self.display_parking_status()
                print(f"\nLast Action: {action}")
                
                time.sleep(update_interval)
                
        except KeyboardInterrupt:
            print("\nSimulation stopped by user")
        
        print("\nSimulation completed!")

def main():
    # Initialize simulation with 3 levels, 10 spots per level
    simulation = ParkingSimulation(num_levels=3, spots_per_level=10)
    
    # Run simulation for 60 seconds with updates every 2 seconds
    simulation.run_simulation(duration_seconds=60, update_interval=2.0)

if __name__ == "__main__":
    main()