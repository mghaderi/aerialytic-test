from abc import ABC, abstractmethod
from typing import Dict, Tuple


class SolarModel(ABC):
    """
    Abstract base class for solar angle calculation models.
    Defines the required interface and shared logic for implementing solar models.
    """

    @abstractmethod
    def calculate_optimal_angles(
        self, latitude: float, longitude: float, offset_angle: float
    ) -> Dict[str, float]:
        """
        Abstract method to compute optimal tilt and azimuth angles for a given location.

        Args:
            latitude (float): Latitude of the location in degrees.
            longitude (float): Longitude of the location in degrees.
            offset_angle (float): Fixed pitch angle of the location in degrees.

        Returns:
            Dict[str, float]: Dictionary with keys 'optimal_pitch' and 'optimal_azimuth'.
        """
        pass

    def _initial_azimuth_pitch(
        self, latitude: float, offset_angle: float
    ) -> Tuple[float, float]:
        """
        Determine initial guess for azimuth and pitch based on latitude and offset.

        - If offset_angle is provided, it overrides pitch.
        - Azimuth is set south (180) in northern hemisphere, north (0) in southern.

        Args:
            latitude (float): Latitude in decimal degrees.
            offset_angle (float): User defined tilt angle.

        Returns:
            tuple[float, float]: (azimuth, pitch)
        """

        azimuth = 180.0 if latitude >= 0 else 0.0
        pitch = offset_angle if offset_angle != 0 else abs(latitude)
        return azimuth, pitch
