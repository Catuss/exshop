from django.db import models
from django.core.urlresolvers import reverse


class Good(models.Model):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['name']

    name = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    content = models.TextField(default='asd')
    image = models.ImageField(upload_to='goods/list', verbose_name='Основное изображение')

    # Если при сохранении изображение меняется
    # старое изображение удаляется
    def save(self, *args, **kwargs):
        try:
            this_rec = Good.objects.get(pk=self.pk)
            if this_rec.image != self.image:
                this_rec.image.delete(save=False)
        except:
            pass
        super(Good, self).save(*args, **kwargs)

    # При удалении записи, удаляется изображение
    # для предотвращения образования "мусора"
    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(Good, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('goods_detail', kwargs={'pk': self.pk})


# Дочерний класс товара, для хранения дополнительных изображений
class GoodImage(models.Model):
    class Meta:
        verbose_name = 'изображение к товару'
        verbose_name_plural = 'изображения к товару'
    good = models.ForeignKey(Good)
    image = models.ImageField(upload_to='goods/detail', verbose_name='Дополнительное изображение')

    # Переопределение метода сохранить, для
    # предотвращения появления "мусора"
    def save(self, *args, **kwargs):
        try:
            this_rec = GoodImage.objects.get(pk=self.pk)
            if this_rec.image != self.image:
                this_rec.image.delete(save=False)
        except:
            pass
        super(GoodImage, self).save(*args, **kwargs)
