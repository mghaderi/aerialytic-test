from solar_calculator.utils.solar_models import SolarModel
from typing import Dict


class NrelCalculatorModel(SolarModel):
    """
    Placeholder implementation for the NREL calculator model.

    Note:
        This is a stub. The current logic only returns initial estimates
        from `_initial_azimuth_pitch`.
        Full integration with the actual NREL model is pending.
    """

    def calculate_optimal_angles(
        self, latitude: float, longitude: float, offset_angle: float
    ) -> Dict[str, float]:
        """
        Compute optimal solar angles using NREL-based logic.

        Args:
            latitude (float): Geographic latitude in degrees.
            longitude (float): Geographic longitude in degrees.
            offset_angle (float): offset angle.

        Returns:
            Dict[str, float]: Stub output with 'optimal_pitch' and 'optimal_azimuth'
            based on initial estimates.
        """
        # TODO: Replace with real NREL implementation when available
        best_azimuth, best_pitch = self._initial_azimuth_pitch(latitude, offset_angle)
        return {
            "optimal_pitch": round(best_pitch, 2),
            "optimal_azimuth": round(best_azimuth, 2),
        }
