from django.views.generic.base import TemplateView
from generic.mixins import Cart_Number_Mixin
from catalog.models import Good
from django.db.models import Q


# Контроллеры для вывода страницы информации о сайте,
# страницы контактов и howtobuy страницы.

class AboutView(Cart_Number_Mixin, TemplateView):
    template_name = 'about.html'


class ContactView(Cart_Number_Mixin, TemplateView):
    template_name = 'contacts.html'


class HowtobuyView(Cart_Number_Mixin, TemplateView):
    template_name = 'howtobuy.html'

class MainPageView(Cart_Number_Mixin, TemplateView):
    template_name = 'main_page.html'

class ResultsSearchView(Cart_Number_Mixin, TemplateView):
    template_name = 'results_search.html'
    def get(self, request, *args, **kwargs):
        self.search = request.GET.get('search')
        self.results = Good.objects.filter(Q(name__icontains=self.search) |
                                        Q(description__icontains=self.search) |
                                        Q(content__icontains=self.search))
        return super(ResultsSearchView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ResultsSearchView, self).get_context_data(**kwargs)
        context['results'] = self.results
        context['numbs'] = [4, 8, 12, 16]
        return context

