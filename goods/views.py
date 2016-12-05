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


# Контроллер вывода списка товаров
class GoodListView(ListView, CategoryListMixin):
    model = Good
    template_name = 'good_index.html'
    paginate_by = 10
    cat = None
    allow_empty = True
    sort_order = 'name'
    instock_order = ''

    # Добавение в контекст текущей категории и параметров сортировки
    def get(self, request, *args, **kwargs):
        if self.kwargs['pk'] is None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk=self.kwargs['pk'])
        try:
            self.sort_order = self.request.GET['order']
        except KeyError:
            pass
        try:
            self.instock_order = self.request.GET['instock']
        except KeyError:
            pass
        return super(GoodListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodListView, self).get_context_data(**kwargs)
        context['category'] = self.cat
        context['order'] = self.sort_order
        context['instock'] = self.instock_order
        return context

    # В зависимости от условий сортировки формируется список объектов
    def get_queryset(self):
        goods = Good.objects.filter(category=self.cat)
        try:
            if self.sort_order == '0price':
                goods = goods.order_by('-price')
            elif self.sort_order == '1price':
                goods = goods.order_by('price')
            elif self.sort_order == 'name':
                goods = goods.order_by('name')
            if self.instock_order == 'true':
                goods = goods.filter(in_stock=True)
        except KeyError:
            pass
        return goods


# Контроллер для показа сведений об отдельном товаре
class GoodDetailView(PageNumberView, DetailView, PageNumberMixin):
    model = Good
    template_name = 'good_detail.html'


# Объявление набора форм для дополнительных изображений товара
GoodImageFormset = inlineformset_factory(Good, GoodImage, can_order=True, fields=['image'])


# Контроллер добавления товара
class GoodCreate(PageNumberView, TemplateView, PageNumberMixin):
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
class GoodUpdate(PageNumberView, TemplateView, PageNumberMixin):
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
class GoodDelete(PageNumberView, DeleteView, PageNumberMixin):
    model = Good
    template_name = 'good_delete.html'

    # Переопределение метода для добавления сообщения об успешном удалении
    def post(self, request, *args, **kwargs):
        self.success_url = reverse('good_index', kwargs={'pk': Good.objects.get(pk=kwargs['pk']).
                                   category.pk}) + '?page=' + self.request.GET['page'] + \
                                    '&sort=' + self.request.GET['sort'] + '&order=' + self.request.GET['order']
        messages.add_message(request, messages.SUCCESS, 'Товар успешно удален')
        return super(GoodDelete, self).post(request, *args, **kwargs)
