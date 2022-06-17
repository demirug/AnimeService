from rest_framework import serializers

from apps.movie.models import Episode, EpisodeFile, Anime, Season, Quality


class QualitySerializer(serializers.ModelSerializer):
    """Serializer for Quality model"""

    class Meta:
        model = Quality
        exclude = ['id']


class FileSerializer(serializers.ModelSerializer):
    """Serializer for EpisodeFile model. Including quality relations"""
    quality = QualitySerializer()
    file = serializers.ReadOnlyField(source='file.url')

    class Meta:
        model = EpisodeFile
        fields = ['file', 'quality']


class EpisodeFileSerializer(serializers.ModelSerializer):
    """Serializer for Episode model. Displaying all files"""
    files = FileSerializer(many=True)

    class Meta:
        model = Episode
        fields = ['number', 'id', 'files']


class EpisodeSerializer(serializers.ModelSerializer):
    """Serializer for Episode model. Displaying all files"""
    url = serializers.HyperlinkedIdentityField(view_name='api:episode-detail', lookup_field='pk')

    class Meta:
        model = Episode
        fields = ['number', 'url']


class SeasonSerializer(serializers.ModelSerializer):
    """Serializer for season model"""
    url = serializers.HyperlinkedIdentityField(view_name='api:season-detail', lookup_field='pk')

    class Meta:
        model = Season
        exclude = ['anime']


class SeasonEpisodeSerializer(SeasonSerializer):
    """Serializer for season model including episode relations"""
    episodes = EpisodeSerializer(many=True)


class AnimeSerializer(serializers.ModelSerializer):
    """Serializer for Anime model. Including season relations"""
    seasons = SeasonSerializer(many=True)

    poster = serializers.ReadOnlyField(source='poster.url')
    url = serializers.HyperlinkedIdentityField(view_name='api:anime-detail', lookup_field='slug')

    class Meta:
        model = Anime
        exclude = ['tag_list', 'style']


class AnimeRandomSerializer(serializers.ModelSerializer):
    """Serializer for random Anime object"""
    poster = serializers.ReadOnlyField(source='poster.url')
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.get_absolute_url()

    class Meta:
        model = Anime
        exclude = ['id', 'tag_list', 'style']
