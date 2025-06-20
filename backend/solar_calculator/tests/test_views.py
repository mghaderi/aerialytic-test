from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class SolarCalculationViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("calculate_solar_angles")

    def test_valid_input_returns_200_and_expected_keys(self):
        data = {"latitude": 45.0, "longitude": -75.0, "offset_angle": 10.0}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("pvlib", response.data)
        self.assertIn("nrel", response.data)
        self.assertIn("liu_jordan", response.data)

        for method in ["pvlib", "nrel", "liu_jordan"]:
            self.assertIn("optimal_pitch", response.data[method])
            self.assertIn("optimal_azimuth", response.data[method])

    def test_offset_angle_is_optional(self):
        data = {"latitude": 45.0, "longitude": -75.0}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_keys_returns_400(self):
        data = {"latitude": 10000, "longitude": 10000, "offset_angle": 10.0}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("latitude", response.data)
        self.assertIn("longitude", response.data)

    def test_missing_keys_returns_400(self):
        data = {
            "latitude": 45.0,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("longitude", response.data)
