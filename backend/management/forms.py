from django import forms
from management.models import AppUtility
import re


class AppUtilityForm(forms.ModelForm):
    class Meta:
        model = AppUtility
        fields = "__all__"
