from django import forms


class GoodAddToCartForm(forms.Form):
    # quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size': '2', 'value': '1',
    #                                                             'class': 'input-small', 'maxlength': '5'}),
    #                               error_messages={'invalid': 'Введите правильное количество'},
    #                               min_value=1, label='Количество')
    good_pk = forms.IntegerField(widget=forms.HiddenInput())
