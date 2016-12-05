from goods.models import Good
from django import forms


# Форма для правки товара
class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['name', 'category', 'description', 'content',
                 'price', 'price_acc', 'in_stock', 'featured', 'image']
    price_acc = forms.IntegerField(required=False, label='Цена со скидкой')
    featured = forms.BooleanField(required=False, label='Рекомендуемый')
    in_stock = forms.BooleanField(required=False, label="В наличии")
    image = forms.ImageField(required=False, label='Картинка')
