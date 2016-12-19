from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Blog(models.Model):
    title = models.CharField(max_length=100, unique_for_date='posted', verbose_name='Заголовок')
    pic = models.ImageField(upload_to='blog', blank=True, null=True, verbose_name='Основное изображение')
    description = models.TextField(verbose_name='Краткое содержание')
    content = models.TextField(verbose_name='Полное содержание')
    posted = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')
    is_commentable = models.BooleanField(default=True, verbose_name='Разрешены комментарии')
    tags = TaggableManager(blank=True, verbose_name='Теги')
    user = models.ForeignKey(User, editable=False)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'pk': self.pk})
