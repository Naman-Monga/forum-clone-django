from django import forms

from . import models

class QuestionForm(forms.Form):
    text = forms.CharField(max_length=4000)
    categories = forms.ModelMultipleChoiceField(queryset=models.Category.objects.all())

class SubmitAnswer(forms.Form):
    text = forms.CharField(max_length=4000)