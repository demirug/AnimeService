from apps.menu.constants import PositionType
from apps.menu.models import Element


def header_objects() -> dict:
    """Template tag for header menu objects"""
    object_list = Element.objects.filter(enabled=True, position=PositionType.HEADER)\
            .order_by("weight", "pk")
    return object_list


def footer_objects() -> dict:
    """Template tag for footer menu objects"""
    object_list = Element.objects.filter(enabled=True, position=PositionType.FOOTER)\
            .order_by("weight", "pk")
    return object_list
