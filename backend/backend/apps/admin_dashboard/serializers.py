from __future__ import annotations

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldDoesNotExist
from django.db.models import FileField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.file_system.fields import generate_thumb, ImageWithThumbsField
from apps.file_system.models import Image
from apps.file_system.settings import THUMBNAIL_SIZES
from apps.notification_system.models import Notification
from utils.serializers import TimestampedSerializer

UserModel = get_user_model()


class ActorSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = UserModel
        fields = ['id', ]


class NotificationSerializer(TimestampedSerializer):
    actor = ActorSerializer()
    verb = serializers.CharField()
    level = serializers.CharField()
    description = serializers.CharField()
    timestamp = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    unread = serializers.BooleanField()
    public = serializers.BooleanField()
    deleted = serializers.BooleanField()
    emailed = serializers.BooleanField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'target', 'verb', 'level', 'description', 'unread', 'public', 'deleted',
                  'emailed', 'timestamp', 'created_at']

    def create(self, validated_data):
        recipient_data = validated_data.pop('recipient')
        recipient = UserModel.objects.get_or_create(id=recipient_data['id'])
        actor_data = validated_data.pop('actor')
        actor = UserModel.objects.get_or_create(id=actor_data['id'])
        notification = Notification.objects.create(recipient=recipient[0], actor=actor[0], **validated_data)
        return notification

    def get_timestamp(self, obj: Notification):
        return get_datetime_formatted(obj.timestamp)


def get_model_field_object(app_name, model_name, model_field_name, object_id):
    model_class = None
    try:
        model_class = apps.get_model(app_name, model_name)
        field: ImageWithThumbsField | FileField = model_class._meta.get_field(model_field_name)
        instance = model_class.objects.get(pk=object_id)
    except LookupError:
        raise serializers.ValidationError("Invalid app_name or model_name", "invalid")
    except FieldDoesNotExist:
        raise serializers.ValidationError("Invalid field name", "invalid")
    except model_class.DoesNotExist:
        raise serializers.ValidationError(f"{model_name} with id={object_id} does not exist", "invalid")
    return model_class, field, instance


class FileUploadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, )
    file = serializers.FileField()
    model_name = serializers.CharField(max_length=100)
    app_name = serializers.CharField(max_length=100)
    method = serializers.ChoiceField(choices=[('attach_field', 'Attach field'), ('attach_model', 'Attach model')])
    type = serializers.ChoiceField(choices=[('thumbnail_image', 'Thumbnail image'), ('file', 'File')])
    object_id = serializers.IntegerField()
    model_field_name = serializers.CharField()

    sizes_width = serializers.IntegerField(required=False)
    sizes_height = serializers.IntegerField(required=False)

    def validate_file(self, value):
        max_file_size = 5 * 1024 * 1024  # 5MB

        if value.size > max_file_size:
            raise serializers.ValidationError("The file size should not exceed 5MB.")

        return value

    def validate_thumbnail_image(self, sizes):
        if (sizes[0] is None) or (sizes[1] is None):
            raise serializers.ValidationError(f"Full size is required")
        if sizes not in THUMBNAIL_SIZES:
            raise serializers.ValidationError(f"Invalid image size. Allowed sizes are: {THUMBNAIL_SIZES}")

    def get_resized_img(self, file, w, h):
        filename_split = file.name.split(".")
        thumb_rel_path = "%s.%sx%s.%s" % (filename_split[:-1], w, h, filename_split[1])
        thumb_content = generate_thumb(img=file, thumb_size=(w, h,), format=filename_split[-1])
        thumb_content.name = thumb_rel_path
        return thumb_rel_path.split("/")[-1], thumb_content, thumb_content

    def create(self, validated_data):
        name = validated_data.get('name')
        file = validated_data.get('file')
        model_name = validated_data.get('model_name')
        app_name = validated_data.get('app_name')
        type_ = validated_data.get('type')
        method = validated_data.get('method')
        object_id = validated_data.get('object_id')
        model_field_name = validated_data.get('model_field_name')
        sizes = None

        if method == 'attach_field':
            if not model_name or not app_name:
                raise serializers.ValidationError("app_name and model_name are required", "required")

        if type_ == 'thumbnail_image':
            sizes = (validated_data.get('sizes_width', None), validated_data.get('sizes_height', None))
            self.validate_thumbnail_image(sizes)

        _, field, instance = get_model_field_object(app_name, model_name, model_field_name, object_id)

        if method == 'attach_model':
            if field.related_model is None:
                raise serializers.ValidationError(f"Field is not related model", "invalid")
            if type_ == 'thumbnail_image':
                if not isinstance(field, Image):
                    raise serializers.ValidationError(f"Field is not 'Image' model", "invalid")
                thumb_file_name, thumb_file_path, thumb_content = self.get_resized_img(file, sizes[0], sizes[1])
                image_obj = Image.objects.create(
                    name=thumb_file_name,
                    url=self.context['request'].build_absolute_uri(
                        serializers.FileField().to_representation(thumb_file_path)),
                )
                setattr(instance, field.name, image_obj)
                instance.save()
        else:
            if type_ == 'thumbnail_image':
                _, _, thumb_content = self.get_resized_img(file, sizes[0], sizes[1])
                setattr(instance, field.name, thumb_content)
                instance.save()
            else:
                setattr(instance, field.name, file)
                instance.save()
        return instance


class FileRemoveSerializer(serializers.Serializer):
    app_name = serializers.CharField(max_length=100)
    model_name = serializers.CharField(max_length=100)
    object_id = serializers.IntegerField()
    model_field_name = serializers.CharField()

    def validate(self, attrs):
        app_name = attrs.get('app_name')
        model_name = attrs.get('model_name')
        object_id = attrs.get('object_id')
        model_field_name = attrs.get('model_field_name')

        attrs['model'], attrs['field'], attrs['instance'] = get_model_field_object(app_name, model_name, model_field_name, object_id)

        return attrs
