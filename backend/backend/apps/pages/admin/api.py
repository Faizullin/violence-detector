from django_restful_admin import admin as api_admin
from rest_framework.viewsets import ModelViewSet

from apps.accounts.permissions import IsAdminOrStaffOrDevloper, permissions
from apps.pages.models import PageDocument, PageStyle
from utils.pagination import DefaultPageNumberWithPageSizePagination
from utils.serializers import TimestampedSerializer


class PageStyleSerializer(TimestampedSerializer):
    class Meta:
        model = PageStyle
        fields = ['id', 'title', 'content']


class EditorSerializer(TimestampedSerializer):
    styles = PageStyleSerializer(many=True, read_only=True)

    class Meta:
        model = PageDocument
        fields = ['id', 'title', 'builder_type', 'content_json', 'styles']


@api_admin.register(PageDocument)
class PageDocumentApiAdmin(ModelViewSet):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [permissions.IsAuthenticated, IsAdminOrStaffOrDevloper]
    pagination_class = DefaultPageNumberWithPageSizePagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EditorSerializer
        return super().get_serializer_class()
