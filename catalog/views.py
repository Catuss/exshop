from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, DeleteView
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from catalog.models import Good, GoodImage
from catalog.forms import GoodForm
from django.db.models import Q
from django.contrib.messages import add_message, INFO
from cart.forms import GoodAddToCartForm
from cart import cart
from generic.mixins import Cart_Number_Mixin


class GoodListView(Cart_Number_Mixin,  ListView):
    """ Контроллер вывода списка товаров """
    model = Good
    template_name = 'catalog.html'
    paginate_by = 1
    allow_empty = True
    sort_order = 'name'

    def get(self, request, *args, **kwargs):
        """
        Метод добавляет в контекст параметры сортировки/поиска

        """
        try:
            self.search = self.request.GET['search']
        except KeyError:
            self.search = ''
        return super(GoodListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodListView, self).get_context_data(**kwargs)
        context['search'] = self.search
        context['numbs'] = [4,8,12]
        return context

    def get_queryset(self):
        """
        QuerySet формируется в зависимости от параметров сортировки

        """
        if self.search:
            try:
                goods = Good.objects.filter(Q(name__icontains=self.search) |
                                   Q(description__icontains=self.search) |
                                   Q(content__icontains=self.search))
                if goods is not None:
                    return goods
                else:
                    add_message(self.request, INFO, 'По вашему запросу ничего не найдено.')
            except:
                pass
        else:
            goods = Good.objects.all()
            return goods


class GoodDetailView(Cart_Number_Mixin, DetailView):
    """ Контроллер выводит страницу отдельного товара """
    model = Good
    template_name = 'detail.html'

    def get(self, request, *args, **kwargs):
        self.cart_product_form = GoodAddToCartForm(initial={'good_pk': kwargs['pk']})
        return super(GoodDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodDetailView, self).get_context_data(**kwargs)
        context['form'] = self.cart_product_form
        return context

    def post(self, request, *args, **kwargs):
        form = GoodAddToCartForm(request.POST)
        if form.is_valid():
            cart.add_to_cart(request)
            return redirect(reverse('cart'))
        else:
            return super(GoodDetailView, self).get(request, *args, **kwargs)


# Объявление набора форм для дополнительных изображений товара
# GoodImageFormset = inlineformset_factory(Good, GoodImage, can_order=True, fields=['image'])

#
# class GoodCreate(TemplateView):
#     """ Контроллер отвечает за создание товара """
#     template_name = 'good_create.html'
#     cat = None
#     form = None
#     formset = None
#
#
#     def get(self, request, *args, **kwargs):
#         self.form = GoodForm(initial={'category': self.cat})
#         self.formset = GoodImageFormset()
#         return super(GoodCreate, self).get(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super(GoodCreate, self).get_context_data(**kwargs)
#         context['category'] = self.cat
#         context['form'] = self.form
#         context['formset'] = self.formset
#         return context
#
#     def post(self, request, *args, **kwargs):
#         """
#         Метод сохраняет форму и набор форм
#
#         """
#         self.form = GoodForm(request.POST, request.FILES)
#         if self.form.is_valid():
#             new_good = self.form.save()
#             self.formset = GoodImageFormset(request.POST, request.FILES, instance=new_good)
#             if self.formset.is_valid():
#                 self.formset.save()
#                 messages.add_message(request, messages.SUCCESS, 'Товар успешно добавлен')
#             return redirect(reverse('good_index', kwargs={'pk': new_good.category.pk}) +
#                             '?page=' + self.request.GET['page'] + '&sort=' +
#                             self.request.GET['sort'] + '&order=' + self.request.GET['order'])
#         self.formset = GoodImageFormset(request.POST, request.FILES)
#         return super(GoodCreate, self).get(request, *args, **kwargs)
#
#
# class GoodUpdate(TemplateView):
#     """ Контроллер правки товара """
#     template_name = 'good_edit.html'
#     good = None
#     form = None
#     formset = None
#
#     def get(self, request, *args, **kwargs):
#         self.good = Good.objects.get(pk=self.kwargs['pk'])
#         self.form = GoodForm(instance=self.good)
#         self.formset = GoodImageFormset(instance=self.good)
#         return super(GoodUpdate, self).get(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super(GoodUpdate, self).get_context_data(**kwargs)
#         context['good'] = self.good
#         context['form'] = self.form
#         context['formset'] = self.formset
#         return context
#
#     def post(self, request, *args, **kwargs):
#         self.good = Good.objects.get(pk=self.kwargs['pk'])
#         self.form = GoodForm(request.POST, request.FILES, instance=self.good)
#         self.formset = GoodImageFormset(request.POST, request.FILES, instance=self.good)
#         if self.form.is_valid():
#             self.form.save()
#             if self.formset.is_valid():
#                 self.formset.save()
#                 messages.add_message(request, messages.SUCCESS, 'Товар успешно изменен')
#             return redirect(reverse('good_index', kwargs={'pk': self.good.category.pk}) +
#                             '?page=' + self.request.GET['page'] + '&sort=' +
#                             self.request.GET['sort'] + '&order=' + self.request.GET['order'])
#         return super(GoodUpdate, self).get(request, *args, **kwargs)
#
#
# class GoodDelete(DeleteView):
#     """ Контроллер отвечает за удаление товара """
#     model = Good
#     template_name = 'good_delete.html'
#
#     def post(self, request, *args, **kwargs):
#         self.success_url = reverse('good_index', kwargs={'pk': Good.objects.get(pk=kwargs['pk']).
#                                    category.pk}) + '?page=' + self.request.GET['page'] + \
#                                     '&sort=' + self.request.GET['sort'] + '&order=' + self.request.GET['order']
#         messages.add_message(request, messages.SUCCESS, 'Товар успешно удален')
#         return super(GoodDelete, self).post(request, *args, **kwargs)
