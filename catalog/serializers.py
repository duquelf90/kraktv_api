from rest_framework import serializers
from catalog.models import YoutubeCatalog


class YoutubeCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeCatalog
        fields = [
            "id",
            "creator",
            "video_url",
            "video_id",
            "title",
            "channel_name",
            "published_at",
            "thumbnail_url",
            "duration",
            "view_count",
            "image_cover",
            "creator_name",
            "category",
            "tags",
            "release_year",
            "genre",
            "subgenre",
            "album_or_series",
            "is_collaboration",
            "composer",
            "producer",
            "created_at",
        ]
