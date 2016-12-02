from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from news.views import NewsListView, NewsDetailView, NewCreate, NewUpdate, NewDelete

# Страницы добавления, правки и удаления новости доступны только если у пользователя есть на это права

urlpatterns = [
    url(r'^$', NewsListView.as_view(), name='news_index'),
    url(r'^(?P<pk>\d+)/$', NewsDetailView.as_view(), name='news_detail'),
    url(r'^add/$', permission_required('news.add_new')(NewCreate.as_view()), name='news_add'),
    url(r'^(?P<pk>\d+)/edit/$', permission_required('news.change_new')(NewUpdate.as_view()), name='news_edit'),
    url(r'^(?P<pk>\d+)/delete/$', permission_required('news.delete_new')(NewDelete.as_view()), name='news_delete'),
]