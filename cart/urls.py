from django.conf.urls import url
from .views import Show_Cart


urlpatterns = [
    url(r'^$', Show_Cart.as_view(), name='cart'),
]