from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from news.models import New
from goods.models import Good


class MainPageView(TemplateView, CategoryListMixin):
    """
     Контроллер отображает список последних новостей и рекомендуемых товаров
    """
    template_name = 'main_page.html'
    news = New.objects.all()[:5]
    goods = Good.objects.filter(featured=True)

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['latest'] = self.news
        context['goods'] = self.goods
        return context

