from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin

# Контроллеры для вывода страницы информации о сайте,
# страницы контактов и howtobuy страницы.
# Использован такой подход, а не статичные страницы Django
# Что бы в контекст шаблона передавался список категорий

class AboutView(TemplateView, CategoryListMixin):
    template_name = 'about.html'


class ContactView(TemplateView, CategoryListMixin):
    template_name = 'contacts.html'


class HowtobuyView(TemplateView, CategoryListMixin):
    template_name = 'howtobuy.html'
