from rest_framework import serializers

from apps.movie.models import Episode, EpisodeFile, Anime, Season, Quality, Review, MovieSettings, Subscribe


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


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = MovieSettings.get_solo()

    def validate_text(self, value: str):
        """Checking if review text larger/lower >= settings params"""
        if len(value) > self.settings.max_review_length:
            raise serializers.ValidationError(f"Maximum length of review text {self.settings.max_review_length} chars")
        if len(value) < self.settings.min_review_length:
            raise serializers.ValidationError(f"Minimum length of review text {self.settings.min_review_length} chars")
        return value

    def validate_season(self, value):
        """Checking if count of user reviews >= settings params"""
        if Review.objects.filter(user=self.context['request'].user,
                                 season_id=value).count() >= self.settings.max_reviews_per_season:
            raise serializers.ValidationError(f"Maximum count of reviews {self.settings.max_reviews_per_season}")
        return value

    class Meta:
        model = Review
        fields = ['season', 'text', 'datetime']


class SubscribeSerializer(serializers.ModelSerializer):
    """Serializer for Subscribe model"""
    class Meta:
        model = Subscribe
        fields = ['anime']
