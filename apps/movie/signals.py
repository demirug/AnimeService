from django.contrib.sites.models import Site
from django.db.models import Avg
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from shared.services.email import send_email
from shared.services.translation import get_field_data_by_user_lang
from .models import Tag, Episode, Rating, Anime, MovieSettings


@receiver(pre_delete, sender=Tag)
def tag_handler(sender, instance: Tag, **kwargs):
    """On Tag delete, delete tag at all Anime objects"""
    for anime in instance.anime.all():
        tags = anime.tags.split(" ")
        tags.remove(instance.name)
        anime.tags = " ".join(tags)
        anime.save()


@receiver(post_save, sender=Episode)
def episode_handler(sender, instance: Episode, **kwargs):
    """On new Episode send email to subscribers"""
    if kwargs.get("created", False):
        anime = instance.season.anime
        subscribers = anime.subscribes.all()

        if subscribers.count() > 0:
            settings: MovieSettings = MovieSettings.get_solo()
            url_path = "{domain}{url}".format(domain=Site.objects.get_current().domain, url=instance.get_absolute_url())

            for subscriber in subscribers:
                # If user language like anime language
                if subscriber.user.lang == anime.lang:
                    title = get_field_data_by_user_lang(settings, subscriber.user, "new_episode_email_title").format(name=anime.name,
                                                                                                                number=instance.number)

                    context = get_field_data_by_user_lang(settings, subscriber.user, "new_episode_email").format(name=anime.name,
                                                                                                            number=instance.number,
                                                                                                            url=url_path)

                    send_email(subscriber.user.email, title, context)


@receiver(post_save, sender=Rating)
def rating_handler(sender, instance: Rating, **kwargs):
    """On Rating update, update anime global rating"""

    anime: Anime = instance.anime
    anime.rating = anime.ratings.filter(val__gt=0).aggregate(Avg("val"))['val__avg']
    anime.save()
