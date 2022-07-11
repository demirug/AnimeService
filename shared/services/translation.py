from django.core.exceptions import FieldDoesNotExist


def get_field_data_by_lang(object, lang: str, fieldName):
    """
    Gets and return field value by name and user language
    Comparable with django-modeltranslator
    param object: object from where fields will be taken
    param lang: language code
    param fieldName: name of field without language code
    return: field value
    """
    try:
        field = object._meta.get_field(fieldName + "_" + lang)
    except FieldDoesNotExist:
        field = object._meta.get_field(fieldName)
    return field.value_from_object(object)
