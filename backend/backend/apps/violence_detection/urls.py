from django.urls import path

from .views import PredictApiView, test_predict, PredictInUserApiView, RecentDetectionsView, RecentDetectionsMapView, \
    MapApiView

app_name = 'violence_detection'

urlpatterns = [
    path("test-predict", test_predict, name="test_predict"),
    path("predictions-news", RecentDetectionsView.as_view(), name="prediction_news_list"),
    path('predictions-news/map', RecentDetectionsMapView.as_view(), name='prediction_news_map'),
    path("api/v1/locations-data/", MapApiView.as_view(), name="locations-data-api"),
    path('api/v1/detector/violence/predict/device', PredictApiView.as_view(), name='predict-api'),
    path('api/v1/detector/violence/predict/user', PredictInUserApiView.as_view(), name='predict-in-user-api'),
]
