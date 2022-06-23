from django.contrib import admin

from apps.helper.forms import AdminQuestionForm
from apps.helper.models import FAQ, Feedback
from shared.services.email import send_email


@admin.register(FAQ)
class DefaultAnswerModelAdmin(admin.ModelAdmin):
    """ModelAdmin for DefaultAnswer model"""
    list_display = ['question', 'slug']


@admin.register(Feedback)
class QuestionModelAdmin(admin.ModelAdmin):
    """ModelAdmin for Question model"""

    form = AdminQuestionForm
    list_display = ('question', 'email', 'answered', 'datetime')
    list_filter = ('answered', 'datetime')
    fieldsets = (
        ('Question', {'fields': ('email', 'question')}),
        ('Answer', {'fields': ('answer',)})
    )
    readonly_fields = ('question', 'email', 'datetime')

    def get_readonly_fields(self, request, obj=None):
        """Add answer to readonly fields if answer given"""
        fields = super(QuestionModelAdmin, self).get_readonly_fields(request, obj)
        if obj.answered:
            fields += ('answer',)
        return fields

    def save_model(self, request, obj, form, change):
        """Send email to user with given answer"""
        if change and obj.answer:
            obj.answered = True
        send_email(obj.email, "Answer on question", "email/helper_answer.jinja",
                   context={"answer": obj.answer, "question": obj.question})

        super(QuestionModelAdmin, self).save_model(request, obj, form, change)

    def has_add_permission(self, request):
        """Disable adding questions"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable deleting questions"""
        return False
