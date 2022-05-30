from django import forms

from apps.movie.models import Review


class ReviewForm(forms.ModelForm):

    text = forms.CharField(label="Text", widget=forms.Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Review
        fields = ['text']