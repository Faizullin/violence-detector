from rest_framework import generics, permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import *
from .serializers import *


class AdminUserNotificationListApiView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filterset_class = NotificationFilter
    pagination_class = BasicPagination
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser  # staff user
    ]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        queryset = Notification.objects.filter(recipient_id=self.request.user.id)
        return queryset


class AdminFileUploadApiView(APIView):
    serializer_class = FileUploadSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        model_instance = serializer.save()
        field = getattr(model_instance, serializer.validated_data.get('model_field_name'))
        file_name = field.name.split('/')[-1]
        return Response({
            "url": request.build_absolute_uri(serializers.FileField().to_representation(field)),
            "relative_path": field.name,
            "name": file_name,
            "object_id": model_instance.pk,
            "model_name": model_instance._meta.model_name,
            "app_name": model_instance._meta.app_label,
            "size": field.size,
        }, status=status.HTTP_201_CREATED)


class AdminFileRemoveApiView(APIView):
    serializer_class = FileRemoveSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.validated_data["instance"]
        field = serializer.validated_data["field"]
        if isinstance(field, ImageWithThumbsField):
            field.delete(save=False)
            setattr(instance, field, None)
        instance.save()
        return Response({
            "success": True,
        }, status=status.HTTP_200_OK)
