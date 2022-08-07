from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = "chat/home.jinja"