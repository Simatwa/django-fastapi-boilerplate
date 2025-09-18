from django import forms

from management.models import AppUtility


class AppUtilityForm(forms.ModelForm):
    class Meta:
        model = AppUtility
        fields = "__all__"
