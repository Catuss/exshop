from django.views.generic.base import ContextMixin, TemplateView
from django.views.generic import ListView, DetailView, DeleteView
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from generic.mixins import CategoryListMixin, PageNumberMixin
from generic.controllers import PageNumberView
from categories.models import Category
from goods.models import Good, GoodImage
from goods.forms import GoodForm


# Добавляет в контекст параметры сортирвки и упорядочивания по умолчанию

class SortMixin(ContextMixin):
    sort = '0'
    order = 'A'

    def get_context_data(self, **kwargs):
        context = super(SortMixin, self).get_context_data(**kwargs)
        context['sort'] = self.sort
        context['order'] = self.order
        return context


# Контроллер вывода списка товаров

class GoodListView(PageNumberView, ListView, SortMixin, CategoryListMixin):
    model = Good
    template_name = 'good_index.html'
    paginate_by = 10
    cat = None
    allow_empty = True

    # Добавляет в контекст текущую категорию, айди категории берется из url

    def get(self, request, *args, **kwargs):
        if self.kwargs['pk'] is None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk=self.kwargs['pk'])
        return super(GoodListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodListView, self).get_context_data(**kwargs)
        context['category'] = self.cat
        return context

    # В зависимости от условий сортировки и упорядочивания
    # формирует список объектов

    def get_queryset(self):
        goods = Good.objects.filter(category=self.cat)
        if self.sort == '2':
            if self.order == 'D':
                goods = goods.order_by('-in_stock', 'name')
            else:
                goods = goods.order_by('in_stock', 'name')
        elif self.sort == '1':
            if self.order == 'D':
                goods = goods.order_by('-price', 'name')
            else:
                goods = goods.order_by('price', 'name')
        else:
            if self.order == "D":
                goods = goods.order_by('-name')
            else:
                goods = goods.order_by('name')
        return goods


# Контроллер для показа сведений об отдельном товаре

class GoodDetailView(PageNumberView, DetailView, SortMixin, PageNumberMixin):
    model = Good
    template_name = 'good_detail.html'


# Объявление набора форм для дополнительных изображений товара
GoodImageFormset = inlineformset_factory(Good, GoodImage, can_order=True, fields=['image'])


# Контроллер добавления товара

class GoodCreate(PageNumberView, TemplateView, SortMixin, PageNumberMixin):
    template_name = 'good_create.html'
    cat = None
    form = None
    formset = None

    # Если категория не указана, берется первая
    # так же формируется объект формы с начальными данными категории
    # и пустой объект набора форм

    def get(self, request, *args, **kwargs):
        if self.kwargs['pk'] is None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk=self.kwargs['pk'])
        self.form = GoodForm(initial={'category': self.cat})
        self.formset = GoodImageFormset()
        return super(GoodCreate, self).get(request, *args, **kwargs)

    # Добавление переменных категории, формы и набора форм в контекст шаблона
    def get_context_data(self, **kwargs):
        context = super(GoodCreate, self).get_context_data(**kwargs)
        context['category'] = self.cat
        context['form'] = self.form
        context['formset'] = self.formset
        return context

    # Cохранение формы и набора форм
    def post(self, request, *args, **kwargs):
        self.form = GoodForm(request.POST, request.FILES)
        if self.form.is_valid():
            new_good = self.form.save()
            self.formset = GoodImageFormset(request.POST, request.FILES, instance=new_good)
            if self.formset.is_valid():
                self.formset.save()
                messages.add_message(request, messages.SUCCESS, 'Товар успешно добавлен')
            return redirect(reverse('good_index', kwargs={'pk': new_good.category.pk}) +
                            '?page=' + self.request.GET['page'] + '&sort=' +
                            self.request.GET['sort'] + '&order=' + self.request.GET['order'])
        if self.kwargs['pk'] is None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk=self.kwargs['pk'])
        self.formset = GoodImageFormset(request.POST, request.FILES)
        return super(GoodCreate, self).get(request, *args, **kwargs)


# Контроллер правки товара

class GoodUpdate(PageNumberView, TemplateView, SortMixin, PageNumberMixin):
    template_name = 'good_edit.html'
    good = None
    form = None
    formset = None

    # Объявление объектов товара, формы и набора форм, заполнение изначальными данными
    def get(self, request, *args, **kwargs):
        self.good = Good.objects.get(pk=self.kwargs['pk'])
        self.form = GoodForm(instance=self.good)
        self.formset = GoodImageFormset(instance=self.good)
        return super(GoodUpdate, self).get(request, *args, **kwargs)

    # Добавление данных в контекст шаблона
    def get_context_data(self, **kwargs):
        context = super(GoodUpdate, self).get_context_data(**kwargs)
        context['good'] = self.good
        context['form'] = self.form
        context['formset'] = self.formset
        return context

    # Сохранение формы и набора форм
    def post(self, request, *args, **kwargs):
        self.good = Good.objects.get(pk=self.kwargs['pk'])
        self.form = GoodForm(request.POST, request.FILES, instance=self.good)
        self.formset = GoodImageFormset(request.POST, request.FILES, instance=self.good)
        if self.form.is_valid():
            self.form.save()
            if self.formset.is_valid():
                self.formset.save()
                messages.add_message(request, messages.SUCCESS, 'Товар успешно изменен')
            return redirect(reverse('good_index', kwargs={'pk': self.good.category.pk}) +
                            '?page=' + self.request.GET['page'] + '&sort=' +
                            self.request.GET['sort'] + '&order=' + self.request.GET['order'])
        return super(GoodUpdate, self).get(request, *args, **kwargs)


# Контроллер удаления товара

class GoodDelete(PageNumberView, DeleteView, SortMixin, PageNumberMixin):
    model = Good
    template_name = 'good_delete.html'

    # Переопределение метода для добавления сообщения об успешном удалении
    def post(self, request, *args, **kwargs):
        self.success_url = reverse('good_index', kwargs={'pk': Good.objects.get(pk=kwargs['pk']).
                                   category.pk}) + '?page=' + self.request.GET['page'] + \
                                    '&sort=' + self.request.GET['sort'] + '&order=' + self.request.GET['order']
        messages.add_message(request, messages.SUCCESS, 'Товар успешно удален')
        return super(GoodDelete, self).post(request, *args, **kwargs)
