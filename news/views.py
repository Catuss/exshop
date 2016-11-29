from django.views.generic.dates import ArchiveIndexView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import add_message, SUCCESS
from news.models import New
from generic.mixins import CategoryListMixin, PageNumberMixin
from generic.controllers import PageNumberView


class NewsListView(ArchiveIndexView, CategoryListMixin):
    model = New
    date_field = 'posted'
    template_name = 'news_index.html'
    paginate_by = 5
    allow_empty = True
    allow_future = True


class NewsDetailView(DetailView, PageNumberMixin):
    model = New
    template_name = 'news_detail.html'


class NewCreate(SuccessMessageMixin, CreateView, CategoryListMixin):
    model = New
    fields = ['title', 'description', 'content']
    template_name = 'new_create.html'
    success_url = reverse_lazy('news_index')
    success_message = 'Новость успешно добавлена'


class NewUpdate(SuccessMessageMixin, PageNumberView, UpdateView, PageNumberMixin,):
    model = New
    fields = ['title', 'description', 'content']
    template_name = 'new_update.html'
    success_url = reverse_lazy('news_index')
    success_message = 'Новость успешно изменена'


class NewDelete(PageNumberView, DeleteView, PageNumberMixin):
    model = New
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_index')

    def post(self, request, *args, **kwargs):
        add_message(request, SUCCESS, 'Новость успешно удалена')
        return super(NewDelete, self).post(request, *args, **kwargs)
