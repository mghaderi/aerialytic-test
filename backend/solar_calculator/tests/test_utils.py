from django.test import TestCase
from solar_calculator.utils.solar_calculator import SolarCalculator


class SolarCalculatorTests(TestCase):
    def setUp(self):
        self.latitude = 45.0
        self.longitude = -75.0
        self.offset_angle = 10.0

    def test_calculate_optimal_angles_structure(self):
        calculator = SolarCalculator(
            latitude=self.latitude,
            longitude=self.longitude,
            offset_angle=self.offset_angle,
        )
        result = calculator.calculate_optimal_angles()

        self.assertIn("pvlib", result)
        self.assertIn("nrel", result)
        self.assertIn("liu_jordan", result)

        for model_key in result:
            self.assertIn("optimal_pitch", result[model_key])
            self.assertIn("optimal_azimuth", result[model_key])
            self.assertIsInstance(result[model_key]["optimal_pitch"], float)
            self.assertIsInstance(result[model_key]["optimal_azimuth"], float)
