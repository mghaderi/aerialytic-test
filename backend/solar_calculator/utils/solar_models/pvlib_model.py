from solar_calculator.utils.solar_models import SolarModel
from typing import Dict, Any
import pandas as pd
from pvlib import irradiance
import numpy as np
from pvlib import location
from timezonefinder import TimezoneFinder


class PvlibCalculatorModel(SolarModel):
    """
    Solar model implementation using the pvlib library.
    Calculates optimal tilt and azimuth angles based on maximizing annual POA irradiance.

    Reference:
        pvlib-python documentation: https://pvlib-python.readthedocs.io/en/stable/
    """

    def calculate_optimal_angles(
        self, latitude: float, longitude: float, offset_angle: float
    ) -> Dict[str, float]:
        """
        Compute optimal solar panel pitch and azimuth
        to maximize irradiance using pvlib.

        Args:
            latitude (float): Geographic latitude.
            longitude (float): Geographic longitude.
            offset_angle (float): Optional fixed tilt value.

        Returns:
            Dict[str, float]: Dictionary with
            'optimal_pitch' and 'optimal_azimuth'.
        """
        timezone = TimezoneFinder().timezone_at(lat=latitude, lng=longitude)
        loc = location.Location(latitude, longitude, tz=timezone)

        times = self._full_year_time_range(timezone)

        solar_positions = loc.get_solarposition(times=times)
        clearsky = loc.get_clearsky(times=times, solar_position=solar_positions)
        best_azimuth, best_pitch = self._initial_azimuth_pitch(latitude, offset_angle)

        # If offset angle is not zero, optimize azimuth only; otherwise, only optimize pitch.
        if offset_angle != 0:
            best_azimuth = self._optimize_azimuth(
                best_azimuth, solar_positions, clearsky, offset_angle
            )
        else:
            best_pitch = self._optimize_pitch(
                best_pitch, best_azimuth, solar_positions, clearsky
            )

        return {
            "optimal_pitch": round(float(best_pitch), 2),
            "optimal_azimuth": round(float(best_azimuth), 2),
        }

    def _full_year_time_range(self, timezone: Any) -> pd.DatetimeIndex:
        """
        Generate hourly timestamps for a full calendar
        year in the given timezone.

        Args:
            timezone (tzinfo): Timezone object.

        Returns:
            pd.DatetimeIndex: Hourly timestamps of current year.
        """
        return pd.date_range(
            start=f"{pd.Timestamp.now().year}-01-01",
            end=f"{pd.Timestamp.now().year}-12-31",
            freq="h",
            tz=timezone,
        )

    def _optimize_azimuth(
        self,
        initial_azimuth: float,
        solar_positions: pd.DataFrame,
        clearsky: pd.DataFrame,
        offset_angle: float,
    ) -> float:
        """
        Find the azimuth angle (0 - 360) that yields
        the highest total annual POA irradiance when pitch is fixed.

        Args:
            initial_azimuth (float): initial azimuth angle.
            solar_positions (pd.DataFrame): Solar position data.
            clearsky (pd.DataFrame): Estimated clear-sky irradiance.
            offset_angle (float): Fixed pitch angle in degrees.

        Returns:
            float: Optimal azimuth angle.
        """
        azimuth_angles_to_test = np.arange(0, 360, 10)
        updated_best_azimuth = initial_azimuth
        max_poa_for_fixed_pitch = -1
        for current_azimuth in azimuth_angles_to_test:
            poa_irradiance = irradiance.get_total_irradiance(
                offset_angle,
                current_azimuth,
                solar_positions["apparent_zenith"],
                solar_positions["azimuth"],
                clearsky["dni"],
                clearsky["ghi"],
                clearsky["dhi"],
                albedo=0.2,
            )
            annual_poa = poa_irradiance["poa_global"].sum()

            if annual_poa > max_poa_for_fixed_pitch:
                max_poa_for_fixed_pitch = annual_poa
                updated_best_azimuth = current_azimuth

        return updated_best_azimuth

    def _optimize_pitch(
        self,
        initial_pitch: float,
        initial_azimuth: float,
        solar_positions: pd.DataFrame,
        clearsky: pd.DataFrame,
    ) -> float:
        """
        Find the pitch angle (0 - 90) that yields the highest total
        annual POA irradiance when azimuth is fixed.

        Args:
            initial_pitch (float): Starting tilt angle.
            initial_azimuth (float): initial azimuth angle.
            solar_positions (pd.DataFrame): Solar position data.
            clearsky (pd.DataFrame): Estimated clear-sky irradiance.

        Returns:
            float: Optimal pitch angle.
        """
        max_annual_poa = -1
        updated_pitch = initial_pitch
        tilt_angles = np.arange(0, 91, 5)
        for current_pitch in tilt_angles:
            poa_irradiance = irradiance.get_total_irradiance(
                current_pitch,
                initial_azimuth,
                solar_positions["apparent_zenith"],
                solar_positions["azimuth"],
                clearsky["dni"],
                clearsky["ghi"],
                clearsky["dhi"],
                albedo=0.2,
            )
            annual_poa = poa_irradiance["poa_global"].sum()
            if annual_poa > max_annual_poa:
                max_annual_poa = annual_poa
                updated_pitch = current_pitch
        return updated_pitch
