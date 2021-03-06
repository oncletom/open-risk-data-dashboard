from rest_framework import serializers
from .models import (
    KeyCategory, KeyDatasetName, KeyTag, KeyTagGroup,
    KeyLevel, KeyDataset)


class KeyLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyLevel
        fields = ('id', 'name')


class KeyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyCategory
        fields = ('id', 'name')


class KeyDatasetNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = KeyDatasetName
        fields = ('id', 'name', 'category')


class KeyTagField(serializers.RelatedField):
    def to_representation(self, value):
        return "%s" % value.name


class KeyTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyTag
        fields = ('group', 'name')


class KeyTagByGroupSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='name')
    tags = serializers.SlugRelatedField(read_only=True, many=True,
                                        slug_field='name')

    class Meta:
        model = KeyTagGroup
        fields = ('group', 'tags')


class KeyDataset0on4Serializer(serializers.ModelSerializer):
    """Partial serializer of key datasets -> level """

    level = KeyLevelSerializer()

    class Meta:
        model = KeyDataset
        fields = ('level',)


class KeyDataset1on4Serializer(serializers.ModelSerializer):
    """Partial serializer of key datasets filtered by level -> category"""

    level = serializers.SlugRelatedField(
        read_only=True, slug_field='name')
    category = KeyCategorySerializer()

    class Meta:
        model = KeyDataset
        fields = ('level', 'category')


class KeyDataset2on4Serializer(serializers.ModelSerializer):
    """Partial serializer of key datasets filtered by level and
       category -> dataset"""

    level = serializers.SlugRelatedField(
        read_only=True, slug_field='name')
    category = serializers.SlugRelatedField(
        read_only=True, slug_field='name')
    dataset = KeyDatasetNameSerializer()

    class Meta:
        model = KeyDataset
        fields = ('level', 'category', 'dataset')


class KeyDataset3on4Serializer(serializers.ModelSerializer):
    """Partial serializer of key datasets filtered by level, category,
       and dataset -> code, description"""

    dataset = KeyDatasetNameSerializer()

    class Meta:
        model = KeyDataset
        fields = ('level', 'category', 'dataset', 'code', 'description')

    def to_representation(self, obj):
        return {
            'level': obj.level.name,
            'category': obj.category.name,
            'dataset': obj.dataset.name,
            'description': {
                'code': obj.code,
                'name': obj.description
                }
            }


class KeyDataset4on4Serializer(serializers.ModelSerializer):
    """Serializer of key datasets filtered by level, category, dataset,
       description"""
    level = serializers.SlugRelatedField(
        read_only=True, slug_field='name')
    category = serializers.SlugRelatedField(
        read_only=True, slug_field='name')
    dataset = KeyDatasetNameSerializer()
    tag_available = KeyTagByGroupSerializer()
    applicability = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field='name')

    class Meta:
        model = KeyDataset
        fields = ('code', 'level', 'category', 'dataset', 'description',
                  'tag_available', 'applicability')
