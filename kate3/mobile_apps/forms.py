from django import forms

from mobile_apps.models import App

class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ('name', 'description', 'educational_uses', 'type', 'cost', 'levels', 'content_areas')

    def save(self, user, *args, **kwargs):
        app = super(AppForm, self).save(commit=False, *args, **kwargs)
        app.user = user
        app.save()