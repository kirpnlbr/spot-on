import os
import time
import random
from typing import Dict
from .engine import ParkingSimulation

class ConsoleVisualizer:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def display_status(simulation: ParkingSimulation, last_action: str = ""): # show status in console
        ConsoleVisualizer.clear_screen()
        status = simulation.get_current_status()
        
        print("\n=== SpotOn Parking System Status ===")
        print(f"Time: {status['timestamp'].strftime('%H:%M:%S')}")
        print("=" * 40)
        
        for level, spots in status['spots_by_level'].items(): # show parking layout
            print(f"\nLevel {level + 1}:")
            print("-" * 20)
            
            for i in range(0, len(spots), 5): # show only 5 spots per line
                line = ""
                for spot in spots[i:i+5]:
                    line += "[X] " if spot.is_occupied else "[ ] "
                print(line)
        
        print("\n=== Statistics ===") # display stats - recharts use case
        print(f"Total Spots: {status['total_spots']}")
        print(f"Occupied Spots: {status['occupied_spots']}")
        print(f"Available Spots: {status['available_spots']}")
        print(f"Occupancy Rate: {status['occupancy_rate']:.1f}%")
        
        if last_action:
            print("\nLast Action:", last_action)
        print("=" * 40)

def run_simulation(duration_seconds: int = 60, update_interval: float = 2.0):
    simulation = ParkingSimulation(num_levels=3, spots_per_level=10)
    
    print(f"\nStarting simulation for {duration_seconds} seconds...")
    print("Press Ctrl+C to stop the simulation")
    
    start_time = time.time()
    try:
        while time.time() - start_time < duration_seconds:
            # simulation time!
            if random.random() < 0.7: # 70% chance of arrival
                vehicle_id, success = simulation.simulate_vehicle_arrival()
                action = f"Vehicle {vehicle_id} arrived and {'found' if success else 'failed to find'} a spot"
            else:
                success = simulation.simulate_vehicle_departure()
                action = f"Vehicle departure was {'successful' if success else 'failed'}"
            
            ConsoleVisualizer.display_status(simulation, action)
            time.sleep(update_interval)
            
    except KeyboardInterrupt:
        print("\nSimulation stopped by user")
    
    print("\nSimulation completed!")

if __name__ == "__main__":
    run_simulation()