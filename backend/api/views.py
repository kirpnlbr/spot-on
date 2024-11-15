from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .core.system import SpotOnSystem
from .simulation.engine import ParkingSimulation
import random

# Initialize the parking system
simulation = ParkingSimulation(num_levels=3, spots_per_level=10)

@api_view(['POST'])
def initialize_parking_lot(request):
    """
    Initialize the parking lot with spots configuration.
    Expected data format:
    [
        {"spot_id": "L1-S1", "level": 1, "distance": 10.0},
        ...
    ]
    """
    spots_config = request.data
    simulation.system.initialize_parking_lot(spots_config)
    return Response({"message": "Parking lot initialized."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def park_vehicle(request):
    """
    Park a vehicle in the nearest available spot.
    Expected data format:
    {"vehicle_id": "V1234", "preferred_level": 1}
    """
    vehicle_id = request.data.get('vehicle_id')
    preferred_level = request.data.get('preferred_level', 0)
    spot_id = simulation.system.park_vehicle(vehicle_id, preferred_level)
    if spot_id:
        return Response({"spot_id": spot_id}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "No available spot."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def remove_vehicle(request):
    """
    Remove a vehicle from its allocated spot.
    Expected data format:
    {"vehicle_id": "V1234"}
    """
    vehicle_id = request.data.get('vehicle_id')
    success = simulation.system.remove_vehicle(vehicle_id)
    if success:
        return Response({"message": "Vehicle removed."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Vehicle not found."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_status(request):
    """
    Retrieve the current status of the parking lot.
    Returns the number of total, occupied, and available spots.
    """
    status_data = simulation.get_current_status()
    status_data['timestamp'] = datetime.now().isoformat()  # Format timestamp as ISO
    return Response(status_data, status=status.HTTP_200_OK)

# New functions to add

@api_view(['GET'])
def get_parking_lots(request):
    """
    Retrieve a list of parking lots (mock data for now).
    """
    parking_lots = [
        {"id": 1, "name": "Central Mall Parking", "distance": "2 mins away", "spots": "12 spots"},
        {"id": 2, "name": "SM Southmall Parking", "distance": "5 mins away", "spots": "8 spots"},
        {"id": 3, "name": "Uptown Parking", "distance": "8 mins away", "spots": "34 spots"},
    ]
    return Response(parking_lots)

@api_view(['GET'])
def get_parking_grid(request, lot_name):
    # Define spots configuration with consistent naming scheme (only A and B rows)
    spots_config = [
        (f"L{level}-A{n}", level - 1, n * 5) for level in range(1, 4) for n in range(1, 6)
    ] + [
        (f"L{level}-B{n}", level - 1, n * 5 + 5) for level in range(1, 4) for n in range(1, 6)
    ]
    
    # Initialize the parking lot with this specific configuration
    simulation.system.initialize_parking_lot(spots_config)

    # Randomly set some spots as occupied
    for spot_id in simulation.system.parking_lot.spots:
        if random.choice([True, False]):
            simulation.system.park_vehicle(vehicle_id=f"V{random.randint(1000, 9999)}", preferred_level=0)
    
    # Prepare data for frontend
    grid_data = [
        {"id": spot_id, "isOccupied": spot.is_occupied}
        for spot_id, spot in simulation.system.parking_lot.spots.items()
    ]
    
    return Response({"name": lot_name, "spots": grid_data})

