from django.views.generic.base import ContextMixin


# Объявление класса добавляющего в контекст шаблона переменную с текущим
# Положением для избегания дублирование кода в контроллерах

class CategoryListMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(CategoryListMixin, self).get_context_data(**kwargs)
        context['current_url'] = self.request.path
        return context