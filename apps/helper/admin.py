from django.contrib import admin
from django.utils.html import format_html, strip_tags
from django.utils.translation import gettext_lazy
from modeltranslation.admin import TranslationAdmin
from solo.admin import SingletonModelAdmin

from apps.helper.forms import FeedbackAdminForm, FAQForm, HelperSettingsForm
from apps.helper.models import FAQ, Feedback, HelperSettings
from shared.services.email import send_email
from shared.services.translation import get_field_data_by_lang


@admin.register(FAQ)
class FAQModelAdmin(TranslationAdmin):
    """ModelAdmin for FAQ model"""
    list_display = ['question']
    form = FAQForm


@admin.register(Feedback)
class FeedbackModelAdmin(admin.ModelAdmin):
    """ModelAdmin for Question model"""

    form = FeedbackAdminForm
    list_display = ('question_strip', 'email', 'answered', 'lang', 'datetime')
    list_filter = ('answered', 'lang', 'datetime')
    fieldsets = (
        ('Question', {'fields': ('email', 'question_format', 'lang', 'datetime')}),
        ('Answer', {'fields': ('answer',)})
    )
    readonly_fields = ('question', 'email', 'datetime', 'question_format')

    def question_strip(self, instance):
        """Remove html tags and limit by 50 chars"""
        quest: str = strip_tags(instance.question)
        if len(quest) > 50:
            return quest[:50] + " ..."
        return quest

    def question_format(self, instance):
        """Insert question to template with html tags"""
        return format_html(instance.question)

    question_strip.short_description = question_format.short_description = gettext_lazy("Question")

    def get_readonly_fields(self, request, obj=None):
        """Add answer to readonly fields if answer given"""
        fields = super().get_readonly_fields(request, obj)
        if obj.answered:
            fields += ('answer',)
        return fields

    def save_model(self, request, obj, form, change):
        """Send email to user with given answer"""
        if change and obj.answer and not obj.answered:
            obj.answered = True

            settings: HelperSettings = HelperSettings.get_solo()
            title: str = get_field_data_by_lang(settings, obj.lang, "feedback_email_title")
            context: str = get_field_data_by_lang(settings, obj.lang, "feedback_email").format(question=obj.question,
                                                                                               answer=obj.answer)
            send_email(obj.email, title, context)

        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        """Disable adding questions"""
        return False


@admin.register(HelperSettings)
class HelperSettingsAdmin(TranslationAdmin, SingletonModelAdmin):
    form = HelperSettingsForm
