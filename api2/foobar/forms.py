from django import forms
from .models import Log, Notify


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ["level", "message"]

class NotifyForm(forms.ModelForm):
    # ts = forms.DateTimeField(blank=False, input_formats=["%Y.%m.%d, %H:%M:%s"])
    class Meta:
        model = Notify
        fields = ["ts", "message"]
