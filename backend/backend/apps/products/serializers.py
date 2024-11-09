from utils.serializers import serializers, TimestampedSerializer
from .models import Product, ProductCategory, Offer, ProductBrand


class OfferSerializer(TimestampedSerializer):
    valid_from = serializers.SerializerMethodField(read_only=True)
    valid_to = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'name', 'valid_from', 'valid_to', 'discount']

    def get_valid_from(self, obj):
        return get_datetime_formatted(obj.valid_from)

    def get_valid_to(self, obj):
        return get_datetime_formatted(obj.valid_to)


class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = ['id', 'slug', 'name', ]


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'slug', 'name', ]


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    brand = ProductBrandSerializer(read_only=True)
    category = ProductCategorySerializer(read_only=True)
    offer = OfferSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'slug', 'name', 'base_price', 'price_of_offer', 'offer',
                  'brand',
                  'category', 'image', 'use_ssr', 'render_url']

    def get_image(self, obj: Product):
        if obj.image:
            return {
                "url": self.context['request'].build_absolute_uri(obj.image.url)
            }


class ProductRetrieveSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    brand = ProductBrandSerializer(read_only=True)
    category = ProductCategorySerializer(read_only=True)
    offer = OfferSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'slug', 'name', 'base_price', 'price_of_offer', 'offer',
                  'brand',
                  'category', 'description', 'image']

    def get_image(self, obj: Product):
        if obj.image:
            return {
                "url": self.context['request'].build_absolute_uri(obj.image.url)
            }
