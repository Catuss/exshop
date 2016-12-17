from django.views.generic.base import View


class PageNumberView(View):
    """
    Класс добавляет локальные переменные поиска и поиска по тегам
    Присваивает им значение из GET запроса, либо пустую строку.

    """
    def get(self, request,  *args, **kwargs):
        try:
            self.search = self.request.GET['search']
        except KeyError:
            self.search = ''
        try:
            self.tag = self.request.GET['tag']
        except KeyError:
            self.tag = ''
        return super(PageNumberView, self).get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        """
        Добавляет к success_url'у страницу пагинатора и параметры поиска

        """
        try:
            pn = request.GET['page']
        except KeyError:
            pn = '1'
            self.success_url = self.success_url + '?page=%s' % pn
        try:
            self.success_url = self.success_url + '&search=' + request.GET['search']
        except KeyError:
            pass
        try:
            self.success_url = self.success_url + '&tag=' + request.GET['tag']
        except KeyError:
            pass
        return super(PageNumberView, self).post(request, *args, **kwargs)
