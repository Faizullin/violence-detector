from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from apps.devices.models import Device

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB in bytes


class PredictionRequestBaseSerializer(serializers.Serializer):
    image = serializers.ImageField()


class Prediction1InputSerializer(serializers.Serializer):
    label = serializers.CharField()
    confidence = serializers.FloatField()


class PredictionRequestSerializer(PredictionRequestBaseSerializer):
    prediction1 = serializers.CharField()
    device_id = PrimaryKeyRelatedField(queryset=Device.objects.all())
    save_to_server = serializers.BooleanField()

    # def validate_image(self, value):
    #
    #     # Check file size
    #     if value.size > MAX_IMAGE_SIZE:
    #         raise serializers.ValidationError(f"Image size should not exceed {MAX_IMAGE_SIZE / (1024 * 1024)} MB")
    #
    #     # Check if the file is a valid image
    #     try:
    #         img = Image.open(io.BytesIO(value.read()))
    #         img.verify()  # Verify it's a valid image
    #     except (IOError, SyntaxError):
    #         raise serializers.ValidationError("Invalid image file")
    #
    #     return value
