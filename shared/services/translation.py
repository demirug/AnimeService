from django.core.exceptions import FieldDoesNotExist

from apps.account.models import User


def get_field_data_by_user_lang(object, user: User, fieldName):
    """
    Gets and return field value by name and user language
    Comparable with django-modeltranslator
    param object: object from where fields will be taken
    param user: user from where language will be taken
    param fieldName: name of field without language code
    return: field value
    """
    try:
        field = object._meta.get_field(fieldName + "_" + user.lang)
    except FieldDoesNotExist:
        field = object._meta.get_field(fieldName)
    return field.value_from_object(object)
