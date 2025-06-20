from rest_framework import serializers


class SolarInputSerializer(serializers.Serializer):
    """
    Input serializer for validating geographic location
    and optional panel tilt.
    """

    latitude = serializers.FloatField(min_value=-90.0, max_value=90.0)
    longitude = serializers.FloatField(min_value=-180.0, max_value=180.0)
    offset_angle = serializers.FloatField(
        required=False, default=0.0, min_value=0.0, max_value=90.0
    )


class SolarOutputSerializer(serializers.Serializer):
    """
    Output serializer for a single model's calculated solar panel angles.
    """

    optimal_pitch = serializers.FloatField(required=True, min_value=0.0, max_value=90.0)
    optimal_azimuth = serializers.FloatField(
        required=True, min_value=0.0, max_value=360.0
    )


class SolarOutputCollectionSerializer(serializers.Serializer):
    """
    Output serializer aggregating results from all implemented solar models.
    """

    pvlib = SolarOutputSerializer()
    nrel = SolarOutputSerializer()
    liu_jordan = SolarOutputSerializer()
