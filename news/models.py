from django.db import models


class New(models.Model):
    class Meta:
        ordering = ['-posted']
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
    title = models.CharField(max_length=100, unique_for_date='posted', verbose_name='Заголовок')
    description = models.TextField(verbose_name='Краткое описание')
    content = models.TextField(verbose_name='Полное содержание')
    posted = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликована')
