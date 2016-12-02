from django import forms
from guestbook.models import GuestBook


# Форма добавления отзыва в гостевую книгу

class GuestBookForm(forms.ModelForm):
    class Meta:
        model = GuestBook
        fields = ['user', 'content', 'honeypot']
    user = forms.CharField(max_length=20, label='Пользователь')
    content = forms.CharField(widget=forms.Textarea, label='Содержание')
    honeypot = forms.CharField(required=False, label='Ловушка для спамеров')
