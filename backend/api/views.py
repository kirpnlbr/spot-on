# backend/api/views.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .core.lotmanager import ParkingLotManager
from django.views.decorators.csrf import csrf_exempt
import random

# Initialize the ParkingLotManager and add multiple parking lots
parking_lot_manager = ParkingLotManager()

# Add three parking lots with varying levels and multilevel configurations
parking_lot_manager.add_parking_lot(
    lot_name="Central Mall Parking",
    num_levels=3,
    is_multi_level=True
)

parking_lot_manager.add_parking_lot(
    lot_name="SM Southmall Parking",
    num_levels=1,
    is_multi_level=False
)

parking_lot_manager.add_parking_lot(
    lot_name="Uptown Parking",
    num_levels=2,
    is_multi_level=True
)

@api_view(['GET'])
def initialize_parking_lot(request, lot_name):
    """
    Re-initialize a specific parking lot with a new random configuration.
    """
    simulation = parking_lot_manager.get_parking_lot(lot_name)
    if not simulation:
        return Response(
            {"error": f"Parking lot '{lot_name}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    simulation.initialize_parking_lot()
    return Response(
        {"message": f"Parking lot '{lot_name}' initialized with random occupancy."},
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def get_parking_grid(request, lot_name):
    """
    Retrieve the parking grid for a specific parking lot and level.
    """
    try:
        print(f"Fetching parking grid for lot: {lot_name}")  # Debug log

        # Get 'level' from the query parameters
        level = request.GET.get("level")
        if level:
            try:
                level = int(level)
                print(f"Requested Level: {level}")  # Debug log
            except ValueError:
                return Response(
                    {"error": "Invalid level parameter. Must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            level = None  # If level is not provided, default to None

        # Get the parking simulation for the requested lot
        simulation = parking_lot_manager.get_parking_lot(lot_name)
        if not simulation:
            return Response(
                {"error": f"Parking lot '{lot_name}' not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get current status
        status_data = simulation.get_current_status()

        # Adjust levels if needed (backend levels are zero-based)
        backend_level = level - 1 if level else None

        # Filter spots by level (if provided)
        grid_data = []
        for lvl, spots in status_data["spots_by_level"].items():
            if backend_level is None or lvl == backend_level:
                grid_data.extend(spots)

        print(f"Returning filtered grid data for Level {level if level else 'All'}:", grid_data)  # Debug log

        return Response({
            "name": lot_name,
            "spots": grid_data,
            "is_multi_level": simulation.is_multi_level,
            "level_layouts": simulation.level_layouts
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print("Error in get_parking_grid:", str(e))  # Error log
        return Response(
            {"error": "An error occurred while fetching the parking grid."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def park_vehicle(request):
    """
    Park a vehicle in the nearest available spot within a specified parking lot.
    """
    vehicle_id = request.data.get('vehicle_id')
    preferred_level = request.data.get('preferred_level', 0)
    lot_name = request.data.get('lot_name')

    if not lot_name:
        return Response(
            {"error": "lot_name is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    simulation = parking_lot_manager.get_parking_lot(lot_name)
    if not simulation:
        return Response(
            {"error": f"Parking lot '{lot_name}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    spot_id = simulation.system.park_vehicle(vehicle_id, preferred_level)
    if spot_id:
        return Response(
            {"spot_id": spot_id},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "No available spot."},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def remove_vehicle(request):
    """
    Remove a vehicle from its allocated spot within a specified parking lot.
    """
    vehicle_id = request.data.get('vehicle_id')
    lot_name = request.data.get('lot_name')

    if not lot_name:
        return Response(
            {"error": "lot_name is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    simulation = parking_lot_manager.get_parking_lot(lot_name)
    if not simulation:
        return Response(
            {"error": f"Parking lot '{lot_name}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    success = simulation.system.remove_vehicle(vehicle_id)
    if success:
        return Response(
            {"message": "Vehicle removed."},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Vehicle not found."},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def get_status(request, lot_name):
    """
    Retrieve the current status of a specific parking lot.
    """
    simulation = parking_lot_manager.get_parking_lot(lot_name)
    if not simulation:
        return Response(
            {"error": f"Parking lot '{lot_name}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    status_data = simulation.get_current_status()
    status_data['timestamp'] = datetime.now().isoformat()

    return Response(status_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_parking_lots(request):
    """
    Retrieve a list of all parking lots with their details.
    """
    parking_lots = []
    for lot_name, simulation in parking_lot_manager.parking_lots.items():
        available_spots = simulation.total_spots - simulation.system.get_total_occupied_spots()
        parking_lots.append({
            "id": lot_name,  # Assuming lot_name is unique; alternatively, use a unique identifier
            "name": lot_name,
            "distance": f"{random.randint(1, 10)} mins away",  # Placeholder; replace with actual data if available
            "spots": f"{available_spots} spots",
            "is_multi_level": simulation.is_multi_level,
            "num_levels": simulation.num_levels,
        })

    return Response(parking_lots, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def start_simulation(request, lot_name):
    """
    Start the simulation for a specific parking lot.
    """
    duration_seconds = request.data.get('duration_seconds', 60)
    update_interval = request.data.get('update_interval', 2)
    arrival_rate = request.data.get('arrival_rate', 0.5)
    departure_rate = request.data.get('departure_rate', 0.5)

    simulation = parking_lot_manager.get_parking_lot(lot_name)
    if not simulation:
        return Response(
            {"error": f"Parking lot '{lot_name}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    if simulation.is_simulation_running:
        return Response(
            {"message": "Simulation is already running."},
            status=status.HTTP_200_OK
        )

    # Optionally, update the rates before starting the simulation
    simulation.arrival_rate = float(arrival_rate)
    simulation.departure_rate = float(departure_rate)

    try:
        parking_lot_manager.start_simulation(lot_name, int(duration_seconds), float(update_interval))
        return Response(
            {"message": f"Simulation started for '{lot_name}' with arrival_rate={arrival_rate} and departure_rate={departure_rate}."},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        print("Error starting simulation:", str(e))  # Error log
        return Response(
            {"error": "Failed to start simulation."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    try:
        arrival_rate = float(arrival_rate)
        departure_rate = float(departure_rate)
        if not (0 <= arrival_rate <= 1) or not (0 <= departure_rate <= 1):
            raise ValueError("Rates must be between 0 and 1.")
        if arrival_rate + departure_rate > 1:
            raise ValueError("The sum of arrival_rate and departure_rate must not exceed 1.")
    except ValueError as ve:
        return Response(
            {"error": str(ve)},
            status=status.HTTP_400_BAD_REQUEST
        )

@csrf_exempt
@api_view(['POST'])
def stop_simulation(request, lot_name):
    """
    Stop the simulation for a specific parking lot.
    """
    simulation = parking_lot_manager.get_parking_lot(lot_name)
    if not simulation:
        return Response(
            {"error": f"Parking lot '{lot_name}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    if not simulation.is_simulation_running:
        return Response(
            {"message": "Simulation is not running."},
            status=status.HTTP_200_OK
        )

    try:
        parking_lot_manager.stop_simulation(lot_name)
        return Response(
            {"message": f"Simulation stopped for '{lot_name}'."},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        print("Error stopping simulation:", str(e))  # Error log
        return Response(
            {"error": "Failed to stop simulation."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def is_simulation_running_view(request, lot_name):
    """
    Check if the simulation is running for a specific parking lot.
    """
    is_running = parking_lot_manager.is_simulation_running(lot_name)
    return Response({"is_running": is_running}, status=status.HTTP_200_OK)
