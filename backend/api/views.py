from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .core.lotmanager import ParkingLotManager
from django.views.decorators.csrf import csrf_exempt
import random
import logging

logger = logging.getLogger(__name__)

parking_lot_manager = ParkingLotManager()

for lot in [
    {"lot_name": "Central Square", "num_levels": 5, "is_multi_level": True, "address": "Central Square 5th Avenue cor. 30th Street Bonifacio Global City, Taguig"},
    {"lot_name": "SM Aura", "num_levels": 1, "is_multi_level": False, "address": "26th Street corner McKinley Parkway, Bonifacio Global City, Taguig"},
    {"lot_name": "Uptown Place Mall", "num_levels": 3, "is_multi_level": True, "address": "9th Ave. corner 36th St., Uptown Bonifacio, The Fort, Taguig"},
    {"lot_name": "Mitsukoshi BGC", "num_levels": 2, "is_multi_level": True, "address": "8th Ave. Corner 36th St., Grand Central Park, 7th Avenue, Taguig"},
]:
    try:
        parking_lot_manager.add_parking_lot(
            lot_name=lot["lot_name"],
            num_levels=lot["num_levels"],
            is_multi_level=lot["is_multi_level"],
            address=lot["address"]
        )
        logger.info(f"Added parking lot: {lot['lot_name']}")
    except ValueError as ve:
        logger.warning(str(ve))


@api_view(['GET'])
def initialize_parking_lot(request, lot_name):
    """
    Re-initialize a specific parking lot with a new random configuration.
    """
    simulation = parking_lot_manager.get_parking_lot(lot_name)
    if not simulation:
        logger.error(f"Parking lot '{lot_name}' not found.")
        return Response(
            {"error": f"Parking lot '{lot_name}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    simulation.initialize_parking_lot()
    logger.info(f"Initialized parking lot '{lot_name}'.")
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
        logger.debug(f"Fetching parking grid for lot: {lot_name}")

        # Get 'level' from the query parameters, default to 1 if not provided
        level_param = request.GET.get("level", "1")
        try:
            level = int(level_param) - 1  # Backend levels are zero-based
            logger.debug(f"Requested Level: {level + 1} (Backend Level: {level})")
        except ValueError:
            logger.error("Invalid level parameter. Must be an integer.")
            return Response(
                {"error": "Invalid level parameter. Must be an integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the parking simulation for the requested lot
        simulation = parking_lot_manager.get_parking_lot(lot_name)
        if not simulation:
            logger.error(f"Parking lot '{lot_name}' not found.")
            return Response(
                {"error": f"Parking lot '{lot_name}' not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate level range
        if level < 0 or level >= simulation.num_levels:
            logger.error(f"Level {level + 1} does not exist in parking lot '{lot_name}'.")
            return Response(
                {"error": f"Level {level + 1} does not exist in parking lot '{lot_name}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Delegate to the ParkingSimulation's get_parking_grid method
        grid_data = simulation.get_parking_grid(lot_name, level)
        if grid_data is None:
            logger.error(f"No grid data available for level {level + 1}.")
            return Response(
                {"error": f"No grid data available for level {level + 1}."},
                status=status.HTTP_404_NOT_FOUND
            )

        logger.info(f"Successfully retrieved parking grid for lot '{lot_name}', level {level + 1}.")
        return Response(grid_data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception(f"Error in get_parking_grid: {str(e)}")
        return Response(
            {"error": "An error occurred while fetching the parking grid."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_parking_lots(request):
    """
    Retrieve a list of all parking lots with their details.
    """
    parking_lots = []
    for lot_name, simulation in parking_lot_manager.parking_lots.items():
        available_spots = simulation.total_spots - simulation.system.get_total_occupied_spots()
        parking_lots.append({
            "id": lot_name,
            "name": lot_name,
            "distance": f"{random.randint(1, 10)} mins away",
            "spots": f"{available_spots} spots",
            "is_multi_level": simulation.is_multi_level,
            "num_levels": simulation.num_levels,
            "address": simulation.address
        })
        logger.debug(f"Added parking lot to list: {lot_name}")

    logger.info("Retrieved list of all parking lots.")
    return Response(parking_lots, status=status.HTTP_200_OK)


@api_view(['POST'])
def park_vehicle(request):
    """
    Park a vehicle in the nearest available spot within a specified parking lot.
    """
    vehicle_id = request.data.get('vehicle_id')
    preferred_level = request.data.get('preferred_level', 0)
    lot_name = request.data.get('lot_name')

    if not lot_name:
        logger.error("lot_name is required.")
        return Response(
            {"error": "lot_name is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    simulation = parking_lot_manager.get_parking_lot(lot_name)
    if not simulation:
        logger.error(f"Parking lot '{lot_name}' not found.")
        return Response(
            {"error": f"Parking lot '{lot_name}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    spot_id = simulation.system.park_vehicle(vehicle_id, preferred_level)
    if spot_id:
        logger.info(f"Vehicle '{vehicle_id}' parked at spot '{spot_id}' in lot '{lot_name}'.")
        return Response(
            {"spot_id": spot_id},
            status=status.HTTP_200_OK
        )
    else:
        logger.warning(f"No available spot for vehicle '{vehicle_id}' in lot '{lot_name}'.")
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
        logger.error("lot_name is required.")
        return Response(
            {"error": "lot_name is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    simulation = parking_lot_manager.get_parking_lot(lot_name)
    if not simulation:
        logger.error(f"Parking lot '{lot_name}' not found.")
        return Response(
            {"error": f"Parking lot '{lot_name}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    success = simulation.system.remove_vehicle(vehicle_id)
    if success:
        logger.info(f"Vehicle '{vehicle_id}' removed from lot '{lot_name}'.")
        return Response(
            {"message": "Vehicle removed."},
            status=status.HTTP_200_OK
        )
    else:
        logger.warning(f"Vehicle '{vehicle_id}' not found in lot '{lot_name}'.")
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
        logger.error(f"Parking lot '{lot_name}' not found.")
        return Response(
            {"error": f"Parking lot '{lot_name}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    status_data = simulation.get_current_status()
    status_data['timestamp'] = datetime.now().isoformat()

    logger.info(f"Retrieved status for parking lot '{lot_name}'.")
    return Response(status_data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def start_simulation(request, lot_name):
    """
    Start the simulation for a specific parking lot.
    """
    duration_seconds = request.data.get('duration_seconds')
    update_interval = request.data.get('update_interval')
    arrival_rate = request.data.get('arrival_rate')
    departure_rate = request.data.get('departure_rate')

    simulation = parking_lot_manager.get_parking_lot(lot_name)
    if not simulation:
        logger.error(f"Parking lot '{lot_name}' not found.")
        return Response(
            {"error": f"Parking lot '{lot_name}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Convert and validate parameters
    try:
        if duration_seconds is not None:
            duration_seconds = int(duration_seconds)
            if duration_seconds <= 0:
                raise ValueError("duration_seconds must be a positive integer.")

        if update_interval is not None:
            update_interval = float(update_interval)
            if update_interval <= 0:
                raise ValueError("update_interval must be a positive number.")

        if arrival_rate is not None:
            arrival_rate = float(arrival_rate)
            if not (0 <= arrival_rate <= 1):
                raise ValueError("arrival_rate must be between 0 and 1.")

        if departure_rate is not None:
            departure_rate = float(departure_rate)
            if not (0 <= departure_rate <= 1):
                raise ValueError("departure_rate must be between 0 and 1.")

        if arrival_rate is not None and departure_rate is not None:
            if arrival_rate + departure_rate > 1:
                raise ValueError("The sum of arrival_rate and departure_rate must not exceed 1.")

    except ValueError as ve:
        logger.error(f"Parameter validation error: {str(ve)}")
        return Response(
            {"error": str(ve)},
            status=status.HTTP_400_BAD_REQUEST
        )

    if simulation.is_simulation_running:
        logger.warning(f"Simulation is already running for lot '{lot_name}'.")
        return Response(
            {"message": "Simulation is already running."},
            status=status.HTTP_200_OK
        )

    try:
        # Start the simulation with provided parameters; defaults are handled in engine.py
        simulation.start_simulation(
            duration_seconds=duration_seconds,
            update_interval=update_interval,
            arrival_rate=arrival_rate,
            departure_rate=departure_rate
        )
        logger.info(f"Started simulation for lot '{lot_name}' with provided parameters.")
        return Response(
            {"message": f"Simulation started for '{lot_name}'."},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        logger.exception(f"Error starting simulation for lot '{lot_name}': {str(e)}")
        return Response(
            {"error": "Failed to start simulation."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@api_view(['POST'])
def stop_simulation(request, lot_name):
    """
    Stop the simulation for a specific parking lot.
    """
    simulation = parking_lot_manager.get_parking_lot(lot_name)
    if not simulation:
        logger.error(f"Parking lot '{lot_name}' not found.")
        return Response(
            {"error": f"Parking lot '{lot_name}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    if not simulation.is_simulation_running:
        logger.warning(f"Simulation is not running for lot '{lot_name}'.")
        return Response(
            {"message": "Simulation is not running."},
            status=status.HTTP_200_OK
        )

    try:
        parking_lot_manager.stop_simulation(lot_name)
        logger.info(f"Stopped simulation for lot '{lot_name}'.")
        return Response(
            {"message": f"Simulation stopped for '{lot_name}'."},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        logger.exception(f"Error stopping simulation for lot '{lot_name}': {str(e)}")
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
    logger.debug(f"Simulation running status for lot '{lot_name}': {is_running}")
    return Response({"is_running": is_running}, status=status.HTTP_200_OK)
