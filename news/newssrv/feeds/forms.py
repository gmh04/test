from django import forms
# from django.forms import ModelForm

# from newssrv.feeds.models import Source

# class EditSource(ModelForm):
#     icon = forms.ImageField(required=False)

#     class Meta:
#         model = Source
#         fields = ('feed_url', 'icon')

class EditSource(forms.Form):
    feed_url = forms.CharField(max_length=128)
    icon = forms.ImageField(required=False)
    
