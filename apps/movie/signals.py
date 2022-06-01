from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Tag


@receiver(pre_delete, sender=Tag)
def tag_handler(sender, instance: Tag, **kwargs):
    """On Tag delete, delete tag at all Anime objects"""
    for anime in instance.anime.all():
        tags = anime.tags.split(" ")
        tags.remove(instance.name)
        anime.tags = " ".join(tags)
        anime.save()
