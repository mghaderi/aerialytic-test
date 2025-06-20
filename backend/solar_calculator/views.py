from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from solar_calculator.serializers import (
    SolarInputSerializer,
    SolarOutputCollectionSerializer,
)
from solar_calculator.utils.solar_calculator import SolarCalculator


class SolarCalculationView(APIView):
    """
    API endpoint to compute optimal solar panel angles using different models.

    Accepts POST requests with latitude, longitude, and optional offset angle.
    Returns pitch and azimuth angles computed by various solar models.
    """

    def post(self, request, format=None):
        """
        Handle POST request to calculate optimal angles.

        Args:
            request (Request): DRF request object containing input data.

        Returns:
            Response: HTTP 200 with serialized model results or
            400 with validation errors.
        """

        serializer = SolarInputSerializer(data=request.data)
        if serializer.is_valid():
            results = SolarCalculator(
                latitude=serializer.validated_data["latitude"],
                longitude=serializer.validated_data["longitude"],
                offset_angle=serializer.validated_data.get("offset_angle", 0.0),
            ).calculate_optimal_angles()
            output_serializer = SolarOutputCollectionSerializer(data=results)
            output_serializer.is_valid(raise_exception=True)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
