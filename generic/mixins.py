from django.views.generic.base import ContextMixin
from categories.models import Category


class CategoryListMixin(ContextMixin):
    """
    Контроллер-примесь добавляет в контекст шаблона список категорий
    и текущее положение, относительно корня сайта

    Список категорий нужен для бокового меню
    Текущее положение для формирования ссылок возврата
    """
    def get_context_data(self, **kwargs):
        context = super(CategoryListMixin, self).get_context_data(**kwargs)
        context['current_url'] = self.request.path
        context['categories'] = Category.objects.order_by('order')
        return context


class PageNumberMixin(CategoryListMixin):
    """
    Добавляет в контекст шаблона переменную текущей, или первой, страницы пацинации

    """
    def get_context_data(self, **kwargs):
        context = super(PageNumberMixin, self).get_context_data(**kwargs)
        try:
            context['pn'] = self.request.GET['page']
        except KeyError:
            context['pn'] = '1'
        return context
