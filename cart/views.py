from django.shortcuts import render, redirect, reverse
from django.views.generic.base import TemplateView
from . import cart

class Show_Cart(TemplateView):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        self.cart_items = cart.get_cart_items(request)
        self.cart_items_count = cart.cart_distinct_item_count(request)
        return super(Show_Cart, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Show_Cart, self).get_context_data(**kwargs)
        context['items'] = self.cart_items
        context['item_count'] = self.cart_items_count
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('input') == 'remove':
            cart.remove_from_cart(request)
        return redirect(reverse('cart'))
