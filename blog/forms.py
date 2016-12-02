from django import forms
from blog.models import Blog


# Обычная форма записи блога

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'content', 'is_commentable', 'tags']