from apps.menu.models import Element


def menu(request):
    """Added menu elements to context"""
    return {
        "menu": Element.objects.filter(enabled=True).order_by("weight", "pk")
    }