from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .simulation.engine import ParkingSimulation
import random

# Initialize the parking simulation with 3 levels and 30 spots per level
simulation = ParkingSimulation(num_levels=3, spots_per_level=30)

@api_view(['GET'])
def initialize_parking_lot(request):
    """
    Re-initialize the parking lot with a new random configuration.
    """
    simulation.initialize_parking_lot()
    return Response({"message": "Parking lot initialized with random occupancy."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_parking_grid(request, lot_name):
    try:
        print("Fetching parking grid for:", lot_name)  # Debugging log
        status_data = simulation.get_current_status()

        # Flatten spots by level into a single list for the frontend
        grid_data = [
            {
                "id": spot["id"],
                "isOccupied": spot["isOccupied"],
                "level": level,
                "distance": spot["distance"],
                "vehicle_id": spot["vehicle_id"],
            }
            for level, spots in status_data["spots_by_level"].items()
            for spot in spots  # Flatten nested list
        ]

        print("Returning grid data:", grid_data)  # Debugging log
        return Response({"name": lot_name, "spots": grid_data}, status=status.HTTP_200_OK)

    except Exception as e:
        print("Error fetching parking grid:", str(e))  # Error log
        return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def park_vehicle(request):
    """
    Park a vehicle in the nearest available spot.
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
    """
    status_data = simulation.get_current_status()
    status_data['timestamp'] = datetime.now().isoformat()
    return Response(status_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_parking_lots(request):
    """
    Retrieve a list of mock parking lots.
    """
    parking_lots = [
        {"id": 1, "name": "Central Mall Parking", "distance": "2 mins away", "spots": "12 spots"},
        {"id": 2, "name": "SM Southmall Parking", "distance": "5 mins away", "spots": "8 spots"},
        {"id": 3, "name": "Uptown Parking", "distance": "8 mins away", "spots": "34 spots"},
    ]
    return Response(parking_lots)
