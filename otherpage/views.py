from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin


class AboutView(TemplateView, CategoryListMixin):
    template_name = 'about.html'


class ContactView(TemplateView, CategoryListMixin):
    template_name = 'contacts.html'


class HowtobuyView(TemplateView, CategoryListMixin):
    template_name = 'howtobuy.html'
