from rest_framework import serializers

from apps.movie.models import Episode, EpisodeFile, Anime, Season, Quality


class SeasonSerializer(serializers.ModelSerializer):
    """Serializer for season model"""

    class Meta:
        model = Season
        exclude = ['id', 'anime']


class AnimeSerializer(serializers.ModelSerializer):
    """Serializer for Anime model. Displaying all seasons"""
    seasons = SeasonSerializer(many=True)
    poster = serializers.ReadOnlyField(source='poster.url')

    class Meta:
        model = Anime
        fields = ['name', 'poster', 'seasons']


class AnimeRandomSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='poster.url')

    class Meta:
        model = Anime
        exclude = ['tag_list', 'style']


class QualitySerializer(serializers.ModelSerializer):
    """Serializer for QualitySerializer model"""

    class Meta:
        model = Quality
        exclude = ['id']


class EpisodeFileSerializer(serializers.ModelSerializer):
    """Serializer for EpisodeFile model. Displaying quality"""
    quality = QualitySerializer()
    file = serializers.ReadOnlyField(source='file.url')

    class Meta:
        model = EpisodeFile
        fields = ['file', 'quality']


class EpisodeSerializer(serializers.ModelSerializer):
    """Serializer for Episode model. Displaying all files"""
    files = EpisodeFileSerializer(many=True)

    class Meta:
        model = Episode
        fields = ['number', 'files']
