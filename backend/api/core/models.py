from dataclasses import dataclass
from typing import Optional

@dataclass
class ParkingSpot:
    """
    Represents a single parking spot in the parking lot.
    
    Attributes:
        id: Unique identifier for the spot
        level: Floor/level number where the spot is located
        distance_from_entrance: Distance from the entrance in arbitrary units
        is_occupied: Whether the spot is currently occupied
        vehicle_id: ID of the vehicle occupying the spot, if any
    """
    id: str
    level: int
    distance_from_entrance: float
    is_occupied: bool = False
    vehicle_id: Optional[str] = None
