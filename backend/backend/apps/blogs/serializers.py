from utils.serializers import TimestampedSerializer, serializers
from .models import BlogPost, UserModel, BlogComment, BlogPostCategory


class BlogAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'first_name', 'last_name')


class BlogPostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostCategory
        fields = ('id', 'slug', 'title')


class BlogPostListSerializer(serializers.ModelSerializer):
    category = BlogPostCategorySerializer(read_only=True)
    author = BlogAuthorSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = ('id', 'slug', 'status', 'author', 'category', 'use_ssr', 'render_url')


class BlogPostRetrieveSerializer(TimestampedSerializer):
    category = BlogPostCategorySerializer(read_only=True)
    author = BlogAuthorSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = (
            'id', 'slug', 'status', 'author', 'category', 'content', 'created_at', 'updated_at',
            'meta_title', 'meta_keywords', 'meta_description', 'use_ssr', 'render_url')


class BlogCommentSerializer(TimestampedSerializer):
    author = BlogAuthorSerializer(read_only=True)

    class Meta:
        model = BlogComment
        fields = ('id', 'author', 'title', 'message', 'created_at', 'updated_at')
