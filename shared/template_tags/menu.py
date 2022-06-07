from apps.menu.models import Element


def menu_objects() -> dict:
    """Template tag for menu elements"""
    return Element.objects.filter(enabled=True).order_by("weight", "pk")
