from typing import Dict
from solar_calculator.utils.solar_models.pvlib_model import PvlibCalculatorModel
from solar_calculator.utils.solar_models.nrel_model import NrelCalculatorModel
from solar_calculator.utils.solar_models.liu_jordan_model import (
    LiuJordanCalculatorModel,
)


class SolarCalculator:
    """
    Main interface to calculate optimal solar panel angles
    using multiple solar modeling approaches.
    """

    def __init__(
        self, latitude: float, longitude: float, offset_angle: float = 0.0
    ) -> None:
        """
        Initialize the calculator with geographic coordinates and optional pitch offset.

        Args:
            latitude (float): Latitude in decimal degrees (-90 to 90).
            longitude (float): Longitude in decimal degrees (-180 to 180).
            offset_angle (float, optional): User-defined fixed tilt angle in degrees (0 to 90). Defaults to 0.0.
        """

        self.latitude: float = latitude
        self.longitude: float = longitude
        self.offset_angle: float = offset_angle

    def calculate_optimal_angles(self) -> Dict[str, Dict[str, float]]:
        """
        Calculate optimal tilt and azimuth angles using different solar models.

        Returns:
            Dict[str, Dict[str, float]]: A dictionary where each key is the model name (e.g., 'pvlib')
            and its value is a dict containing 'optimal_pitch' and 'optimal_azimuth'.
        """
        return {
            "pvlib": PvlibCalculatorModel().calculate_optimal_angles(
                latitude=self.latitude,
                longitude=self.longitude,
                offset_angle=self.offset_angle,
            ),
            "nrel": NrelCalculatorModel().calculate_optimal_angles(
                latitude=self.latitude,
                longitude=self.longitude,
                offset_angle=self.offset_angle,
            ),
            "liu_jordan": LiuJordanCalculatorModel().calculate_optimal_angles(
                latitude=self.latitude,
                longitude=self.longitude,
                offset_angle=self.offset_angle,
            ),
        }
