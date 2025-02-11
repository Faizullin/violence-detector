import json

import django_filters
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from rest_framework import permissions, status, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from apps.devices.models import Device
from apps.file_system.models import File
from .models import News, Prediction, PredictionAttempt

use_detection = settings.USE_VIOLENCE_DETECTION
if use_detection:
    from .serializers import (PredictionRequestBaseSerializer,
                              PredictionRequestSerializer)
    from .violence_detection.utils.image import imdecode
    from .violence_detection.violence_alarm_detection.detector import \
        ViolenceAlarmDetector

    # removed because to heavy
    # from .violence_detection.violence_basic_detection.detector import \
    #     ViolenceBasicDetector

    # basic_detector = ViolenceBasicDetector()
    # basic_detector.load_model_and_prepare()
    alarm_detector = ViolenceAlarmDetector()
    alarm_detector.load_model_and_prepare()


def generate_news_for_prediction_attempt(obj: PredictionAttempt):
    news_obj = News.objects.create(
        author=obj.device.user,
        prediction_attempt=obj,
        title="",
    )
    news_obj.title = "Инцидент " + str(news_obj.id)

    preds = news_obj.prediction_attempt.prediction_set.all()
    if len(preds) != 2:
        raise ValueError("Incorrect number of predictions in database.")
    news_obj.description = f'''
    Предсказания: \n
    {str(preds[0].type)}: {preds[0].message} {str(preds[0].confidence)}\n
    {str(preds[1].type)}: {str(preds[1].message)} {str(preds[1].confidence)}\n
    '''
    news_obj.save()
    return news_obj


class PredictApiView(APIView):
    permission_classes = (HasAPIKey,)

    def post(self, request):
        serializer = PredictionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device: Device = serializer.validated_data.get("device_id")
        save_to_server = serializer.validated_data.get("save_to_server")
        prediction1 = request.data.get("prediction1", None)
        prediction1 = json.loads(prediction1)

        if save_to_server:
            device.last_active = timezone.now()
            device.save()
        image_file = serializer.validated_data.get("image")
        image_buf = image_file.read()
        if not len(image_buf):
            return Response({
                "message": "File empty error!",
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            image = imdecode(image_buf)
        except:
            return Response({
                "message": "Image format error!",
            }, status=status.HTTP_400_BAD_REQUEST)

        # prediction1 = basic_detector.detect_image(image)
        prediction2 = alarm_detector.detect_image(image)
        is_to_save = bool(self.is_to_save([prediction1], prediction2) and save_to_server)

        if is_to_save:
            file_obj = File.objects.create(file=image_file)
            file_obj.save()
            prediction_attempt_obj = PredictionAttempt.objects.create(
                device=device,
                device_name=device.name,
                image=file_obj,
            )
            prediction1_obj = Prediction.objects.create(
                type="basic",
                attempt=prediction_attempt_obj,
                device=prediction_attempt_obj.device,
                result=str(prediction1),
                confidence=float(prediction1["prediction"]["confidence"]),
                message=prediction1["prediction"]["label"],
                description="",
            )
            prediction2_obj = Prediction.objects.create(
                type="alarm",
                attempt=prediction_attempt_obj,
                device=prediction_attempt_obj.device,
                result=str(prediction2),
                confidence=float(prediction2[0]["prediction"]),
                message=prediction2[0]["message"],
                description="",
            )
        else:
            prediction_attempt_obj = None

        news_saved = False
        if is_to_save and prediction_attempt_obj is not None and device.news_create_allowed:
            generate_news_for_prediction_attempt(prediction_attempt_obj)
            news_saved = True

        return Response({'data': {
            "saved": is_to_save,
            "news_saved": news_saved,
            "prediction_attempt_obj": None if prediction_attempt_obj is None else {
                "id": prediction_attempt_obj.id,
            },
            "pred": {
                "prediction1": prediction1,
                "prediction2": prediction2,
            }
        }})

    def is_to_save(self, prediction1, prediction2):
        prediction1_data = prediction1[0]
        prediction1_keywords = ["violence", "fire", "fight", "crash"]
        p1_viol = False
        for i in prediction1_keywords:
            if i in prediction1_data["prediction"]["label"]:
                p1_viol = True
                break

        prediction2_data = prediction2[0]
        p2_viol = prediction2_data["result"]
        return p1_viol or p2_viol
        if p1_viol and not p2_viol:
            return False
        elif p1_viol and p2_viol:
            return True
        elif not p1_viol and p2_viol:
            return True
        else:
            return False


class PredictInUserApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = PredictionRequestBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image_file = serializer.validated_data.get("image")
        image_buf = image_file.read()
        if not len(image_buf):
            return Response({
                "message": "File empty error!",
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            image = imdecode(image_buf)
        except:
            return Response({
                "message": "Image format error!",
            }, status=status.HTTP_400_BAD_REQUEST)

        # prediction1 = basic_detector.detect_image(image)
        prediction2 = alarm_detector.detect_image(image)

        return Response({'data': {
            "pred": {
                # "prediction1": str(prediction1),
                "prediction2": str(prediction2),
            }
        }})


@login_required
def test_predict(request):
    return render(request, "violence_detection/test_predict.html")


def get_news_qs():
    return News.objects.order_by('-updated_at').prefetch_related(
        "prediction_attempt").prefetch_related("prediction_attempt__prediction_set")


class RecentDetectionsView(ListView):
    # model = News
    template_name = "violence_detection/news_list.html"
    context_object_name = "latest_available_news"

    # paginate_by = 1

    def get_queryset(self):
        return get_news_qs()


class RecentDetectionsMapView(ListView):
    # model = News
    template_name = "violence_detection/news_map.html"
    context_object_name = "latest_available_news"

    # paginate_by = 1

    def get_queryset(self):
        return get_news_qs()

    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context.update({
            "devices": Device.objects.all(),
        })
        return context


class NewsSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source="prediction_attempt.device_name", read_only=True)
    lat = serializers.FloatField(source="prediction_attempt.lat", read_only=True)
    lang = serializers.FloatField(source="prediction_attempt.lang", read_only=True)
    device_id = serializers.CharField(source="prediction_attempt.device_id", read_only=True)

    class Meta:
        model = News
        fields = ["title", "description", "device_id", "device_name", "lat", "lang", "created_at", "updated_at"]


class NewsFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="updated_at", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="updated_at", lookup_expr="lte")
    device_id = django_filters.CharFilter(field_name="prediction_attempt__device")

    class Meta:
        model = News
        fields = ["start_date", "end_date", "device_id"]


class MapApiView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = get_news_qs()

        # Apply filters
        filterset = NewsFilter(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs

        # Apply ordering
        ordering_backend = OrderingFilter()
        queryset = ordering_backend.filter_queryset(request, queryset, self)

        serializer = NewsSerializer(queryset, many=True)
        return Response(serializer.data)
