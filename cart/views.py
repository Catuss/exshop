from django.shortcuts import redirect, reverse
from django.views.generic.base import TemplateView
from . import cart
from .forms import SetOrderForm
from .models import Order

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


class Set_Order(TemplateView):
    template_name = 'set_order.html'

    def get(self, request, *args, **kwargs):
        self.order_goods = cart.get_cart_items(request)
        self.form = SetOrderForm()
        return super(Set_Order, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Set_Order, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['items'] = self.order_goods
        return context

    def post(self, request, *args, **kwargs):
        form = SetOrderForm(request.POST)
        if form.is_valid():
            order_goods = cart.get_cart_items(request)
            cd = form.cleaned_data
            good_list = [str(i.good.id) for i in order_goods]
            order = Order.objects.create(order_location=cd['order_location'], order_name=cd['order_name'],
                                         order_email=cd['order_email'], order_goods=good_list,
                                         order_phone_number=['order_phone_number'])
            return redirect(reverse('success'))
        else:
            return redirect(reverse('order'))


class Success_Buy(TemplateView):
    template_name = 'success_buy.html'
