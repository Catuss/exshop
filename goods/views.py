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
from django.db.models import Q
from django.contrib.messages import add_message, INFO


class GoodListView(ListView, CategoryListMixin):
    """ Контроллер вывода списка товаров """
    model = Good
    template_name = 'good_index.html'
    paginate_by = 10
    cat = None
    allow_empty = True
    sort_order = 'name'
    instock_order = ''

    def get(self, request, *args, **kwargs):
        """
        Метод добавляет в контекст категорию  и параметры сортировки/поиска

        """
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
        try:
            self.search = self.request.GET['search']
        except KeyError:
            self.search = ''
        return super(GoodListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodListView, self).get_context_data(**kwargs)
        context['category'] = self.cat
        context['order'] = self.sort_order
        context['instock'] = self.instock_order
        context['search'] = self.search
        return context

    def get_queryset(self):
        """
        QuerySet формируется в зависимости от параметров сортировки

        """
        try:
            goods = Good.objects.filter(Q(name__icontains=self.search) |
                               Q(description__icontains=self.search) |
                               Q(content__icontains=self.search))
            if goods.count() < 1:
                add_message(self.request, INFO, 'По вашему запросу ничего не найдено.')
            return goods
        except:
            pass

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


class GoodDetailView(PageNumberView, DetailView, PageNumberMixin):
    """ Контроллер выводит страницу отдельного товара """
    model = Good
    template_name = 'good_detail.html'


# Объявление набора форм для дополнительных изображений товара
GoodImageFormset = inlineformset_factory(Good, GoodImage, can_order=True, fields=['image'])


class GoodCreate(PageNumberView, TemplateView, PageNumberMixin):
    """ Контроллер отвечает за создание товара """
    template_name = 'good_create.html'
    cat = None
    form = None
    formset = None


    def get(self, request, *args, **kwargs):
        if self.kwargs['pk'] is None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk=self.kwargs['pk'])
        self.form = GoodForm(initial={'category': self.cat})
        self.formset = GoodImageFormset()
        return super(GoodCreate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodCreate, self).get_context_data(**kwargs)
        context['category'] = self.cat
        context['form'] = self.form
        context['formset'] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        """
        Метод сохраняет форму и набор форм

        """
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


class GoodUpdate(PageNumberView, TemplateView, PageNumberMixin):
    """ Контроллер правки товара """
    template_name = 'good_edit.html'
    good = None
    form = None
    formset = None

    def get(self, request, *args, **kwargs):
        self.good = Good.objects.get(pk=self.kwargs['pk'])
        self.form = GoodForm(instance=self.good)
        self.formset = GoodImageFormset(instance=self.good)
        return super(GoodUpdate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodUpdate, self).get_context_data(**kwargs)
        context['good'] = self.good
        context['form'] = self.form
        context['formset'] = self.formset
        return context

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


class GoodDelete(PageNumberView, DeleteView, PageNumberMixin):
    """ Контроллер отвечает за удаление товара """
    model = Good
    template_name = 'good_delete.html'

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('good_index', kwargs={'pk': Good.objects.get(pk=kwargs['pk']).
                                   category.pk}) + '?page=' + self.request.GET['page'] + \
                                    '&sort=' + self.request.GET['sort'] + '&order=' + self.request.GET['order']
        messages.add_message(request, messages.SUCCESS, 'Товар успешно удален')
        return super(GoodDelete, self).post(request, *args, **kwargs)
