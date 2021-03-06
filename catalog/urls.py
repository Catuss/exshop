from django.conf.urls import url
from catalog.views import GoodListView, GoodDetailView # , GoodCreate, GoodUpdate, GoodDelete
from django.contrib.auth.decorators import permission_required


# Правка товаров доступна только пользователям с соответствующими правами
urlpatterns = [
    url(r'^$', GoodListView.as_view(), name='catalog'),
    url(r'^(?P<pk>\d+)/$', GoodDetailView.as_view(), name='good_detail'),
    # url(r'^(?P<pk>\d+)/add/$', permission_required('goods.add_good')
    # (GoodCreate.as_view()), name='good_create'),
    # url(r'^(?P<pk>\d+)/edit/$', permission_required('goods.change_good')
    # (GoodUpdate.as_view()), name='good_edit'),
    # url(r'^(?P<pk>\d+)/delete/$', permission_required('goods.delete_good')
    # (GoodDelete.as_view()), name='good_delete'),
]

