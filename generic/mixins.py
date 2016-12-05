from django.views.generic.base import ContextMixin
from categories.models import Category

# Класс добавляет в контекст шаблона список категорий и текущий путь относительно корня сайта
class CategoryListMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(CategoryListMixin, self).get_context_data(**kwargs)
        context['current_url'] = self.request.path
        context['categories'] = Category.objects.order_by('order')
        return context


# Наследуется от класса-предка ListView
# Добавляет в контекст шаблона текущую страницу пагинатора
class PageNumberMixin(CategoryListMixin):
    def get_context_data(self, **kwargs):
        context = super(PageNumberMixin, self).get_context_data(**kwargs)
        try:
            context['pn'] = self.request.GET['page']
        except KeyError:
            context['pn'] = '1'
        return context
