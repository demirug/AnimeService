from django.conf import settings


class TranslateFormWidgetMixin:
    """Set widgets for translated fields"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load languages and widgets
        languages = [tpl[0] for tpl in settings.LANGUAGES]
        widgets = self.get_widgets()

        for field in self.fields:
            data = str(field).split("_")

            # Check data valid and given language exists
            if len(data) > 1 and data[-1] in languages:
                field_name = "_".join(data[:-1])
                # Check if widget given
                if field_name in widgets:
                    self.fields[field].widget = widgets[field_name]

    def get_widgets(self) -> dict:
        """
        Return dict with fields & widgets
        :example return {"fieldname_without_lang_tag": CKEditorWidget()}
        """
        return {}