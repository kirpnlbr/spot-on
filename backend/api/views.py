from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .core.system import SpotOnSystem
from .simulation.engine import ParkingSimulation

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
