from django.contrib.sites.models import Site
from django.db.models import Sum, Avg
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from shared.services.email import send_email
from .models import Tag, Episode, Rating, Anime


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
        subscribers = list(anime.subscribes.values_list("user__email", flat=True))
        if len(subscribers) == 0:
            return

        send_email(subscribers, _(f"New Episode {anime.name} #{instance.number}"), "email/new_episode.jinja",
                   context={"url": "{domain}{url}".format(domain=Site.objects.get_current().domain,
                                                          url=instance.get_absolute_url()),
                            "episode": instance,
                            "anime": anime,
                            })


@receiver(post_save, sender=Rating)
def rating_handler(sender, instance: Rating, **kwargs):
    """On Rating update, update anime global rating"""

    anime: Anime = instance.anime
    anime.rating = anime.ratings.filter(val__gt=0).aggregate(Avg("val"))['val__avg']
    anime.save()