from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView

from apps.helper.forms import AuthorizeQuestionForm, UnAuthorizeQuestionForm
from apps.helper.models import FAQ, Feedback
from shared.mixins.breadcrumbs import BreadCrumbsMixin


class AnswersQuestionsView(BreadCrumbsMixin, CreateView):
    """ListView for DefaultAnswer with creating Questions objects"""
    model = Feedback
    template_name = "helper/home.jinja"

    def get_breadcrumbs(self):
        return [(_("Home"), reverse("home")), (_("Questions"),)]

    def get_form_class(self):
        """Return form depending on player authorization status"""
        if self.request.user.is_authenticated:
            return AuthorizeQuestionForm
        else:
            return UnAuthorizeQuestionForm

    def form_valid(self, form):
        question = form.save(commit=False)
        if type(form) == AuthorizeQuestionForm:
            question.email = self.request.user.email
        question.save()

        messages.success(self.request, _("Your question has been sent. Check your email for a reply"))
        return redirect("helper")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = FAQ.objects.all()
        return context