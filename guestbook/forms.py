from django import forms
from guestbook.models import GuestBook


class GuestBookForm(forms.ModelForm):
    """ Форма для оставления отзыва в гостевой книге """
    class Meta:
        model = GuestBook
        fields = ['user', 'content', 'honeypot']
    user = forms.CharField(max_length=20, label='Name')
    content = forms.CharField(widget=forms.Textarea, label='Text')
    honeypot = forms.CharField(required=False, label='Ловушка для спамеров')
