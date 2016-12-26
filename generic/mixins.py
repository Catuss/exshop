from django.views.generic.base import ContextMixin
from cart.cart import cart_distinct_item_count, get_cart_items


class Cart_Number_Mixin(ContextMixin):

    def get(self, request, *args, **kwargs):
        self.cart_count = cart_distinct_item_count(request)
        self.cart_item = [ i.good for i in get_cart_items(request)]
        return super(Cart_Number_Mixin, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Cart_Number_Mixin, self).get_context_data(**kwargs)
        context['cart_count'] = self.cart_count
        context['cart_item'] = self.cart_item
        return context
