from django import forms
from cart.models import Order

class GoodAddToCartForm(forms.Form):
    # quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size': '2', 'value': '1',
    #                                                             'class': 'input-small', 'maxlength': '5'}),
    #                               error_messages={'invalid': 'Введите правильное количество'},
    #                               min_value=1, label='Количество')
    good_pk = forms.IntegerField(widget=forms.HiddenInput())


class SetOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_name', 'order_location', 'order_phone_number', 'order_email']
        labels = {'order_name': 'Name', 'order_location': 'Address',
                  'order_phone_number': 'Phone number',  'order_email': 'Email'}