from django.views.generic import ArchiveIndexView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import add_message, SUCCESS, INFO

from news.models import New
from generic.mixins import CategoryListMixin, PageNumberMixin
from generic.controllers import PageNumberView
from django.db.models import Q


# Контроллер вывода списка новостей отсортированных по дате

class NewsListView(PageNumberView, ArchiveIndexView, CategoryListMixin):
    model = New
    date_field = 'posted'
    template_name = 'news_index.html'
    paginate_by = 10
    allow_empty = True
    allow_future = True

    def get_queryset(self):
        queryset = super(NewsListView, self).get_queryset()
        try:
            search = self.request.GET['search']
            queryset = New.objects.filter(Q(title__icontains=search) |
                               Q(description__icontains=search) |
                               Q(content__icontains=search))
            if queryset.count() < 1:
                add_message(self.request, INFO, 'По вашему запросу ничего не найдено.')
        except KeyError:
            return queryset
        return queryset




# Контроллер вывода подробностей новости
# PageNumberMixin в списке родителей добавляет в url страницу пагинации,
# Что бы пользователь при нажатии кнопки назад вернулся на прежнюю страницу

class NewsDetailView(DetailView, PageNumberMixin):
    model = New
    template_name = 'news_detail.html'


# Контроллер создания новости

class NewCreate(SuccessMessageMixin, CreateView, CategoryListMixin):
    model = New
    fields = ['title', 'description', 'content']
    template_name = 'new_create.html'
    success_url = reverse_lazy('news_index')
    success_message = 'Новость успешно добавлена'


# Контроллер редактирования новости

class NewUpdate(SuccessMessageMixin, PageNumberView, UpdateView, PageNumberMixin,):
    model = New
    fields = ['title', 'description', 'content']
    template_name = 'new_update.html'
    success_url = reverse_lazy('news_index')
    success_message = 'Новость успешно изменена'


# Контроллер удаления новости

class NewDelete(PageNumberView, DeleteView, PageNumberMixin):
    model = New
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_index')

    def post(self, request, *args, **kwargs):
        add_message(request, SUCCESS, 'Новость успешно удалена')
        return super(NewDelete, self).post(request, *args, **kwargs)
