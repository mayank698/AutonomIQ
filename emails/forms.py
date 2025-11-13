from django import forms
from .models import Email


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = "__all__"
        widgets = {
            "body": forms.Textarea(attrs={"rows": 4}),
            # Add any other textarea fields from your Email model
        }
