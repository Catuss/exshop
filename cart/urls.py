from django.conf.urls import url
from .views import Show_Cart, Set_Order, Success_Buy


urlpatterns = [
    url(r'^$', Show_Cart.as_view(), name='cart'),
    url(r'^order/$', Set_Order.as_view(), name='order'),
    url(r'^success/$', Success_Buy.as_view(), name='success'),
]