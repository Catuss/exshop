from django.views.generic.base import TemplateView
from django.views.generic import ArchiveIndexView, DetailView, CreateView, DeleteView
from generic.mixins import CategoryListMixin, PageNumberMixin
from generic.controllers import PageNumberView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect

from blog.forms import BlogForm
from blog.models import Blog
from django.db.models import Q


class BlogListView(ArchiveIndexView, CategoryListMixin):
    """
    Контроллер отвечает за вывод списка постов

    """
    model = Blog
    date_field = 'posted'
    template_name = 'blog_index.html'
    paginate_by = 10
    allow_empty = True
    allow_future = True


    def get_queryset(self):
        """
        Если указаны параметры поиска
        возвращает список соответствующих записей, или сообщение об ошибке
        """
        blog = super(BlogListView, self).get_queryset()
        try:
            search = self.request.GET['search']
            blog = blog.filter(Q(title__icontains=search) |
                               Q(description__icontains=search) |
                                 Q(content__icontains=search))
            if blog.count() < 1:
                messages.add_message(self.request, messages.INFO, 'По вашему запросу ничего не найдено.')
        except KeyError:
            return blog
        try:
            tag = self.request.GET['tag']
            blog = blog.filter(tags__name=tag)
            if blog.count() < 1:
                messages.add_message(self.request, messages.INFO, 'По вашему запросу ничего не найдено.')
        except KeyError:
            return blog
        return blog


class BlogDetailView(PageNumberView, DetailView,  PageNumberMixin):
    """ Контроллер отображает страницу отдельного поста """
    model = Blog
    template_name = 'blog_detail.html'
    

class BlogCreate(SuccessMessageMixin, CreateView, CategoryListMixin):
    """ Контроллер для создания записи """
    form_class = BlogForm
    model = Blog
    template_name = 'blog_create.html'
    success_url = reverse_lazy('blog_index')
    success_message = 'Статья успешно создана'

    def form_valid(self, form):
        """
         Метод подставляет в поле автора текущего юзера

        """
        form.instance.user = self.request.user
        return super(BlogCreate, self).form_valid(form)


class BlogDelete(PageNumberView, DeleteView, PageNumberMixin):
    """ Контроллер удаления записи """
    model = Blog
    template_name = 'blog_delete.html'
    success_url = reverse_lazy('blog_index')

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS, 'Пост успешно удален')
        return super(BlogDelete, self).post(request, *args, **kwargs)


class BlogUpdate(PageNumberView, TemplateView,  PageNumberMixin):
    """ Контроллер правки записи """
    blog = None
    template_name = 'blog_edit.html'
    form = None

    # Выводит форму только если пользователь является автором, или суперпользователем
    # Иначе редиректит на страницу логина
    def get(self, request,  *args, **kwargs):
        """
        Отображает форму только если пользователь является автором записи, или суперпользователем

        """
        self.blog = Blog.objects.get(pk=self.kwargs['pk'])
        if self.blog.user == request.user or request.user.is_superuser:
            self.form = BlogForm(instance=self.blog)
            return super(BlogUpdate, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    def get_context_data(self, **kwargs):
        context = super(BlogUpdate, self).get_context_data(**kwargs)
        context['blog'] = self.blog
        context['form'] = self.form
        return context

    # Заполнение и отправка формы с дополнительной проверкой, является ли пользователь
    # автором или суперпользователем.
    # Редирект на страницу с которой пришел пользователь, с учетом параметров поиска, пагинации и тегов
    # Если пользователь не автор и не суперпользователь - редирект на страницу регистрации
    def post(self, request, *args, **kwargs):
        """
        Дополнительная проверка, является ли пользователь автором поста или суперпользователем
        Сохранение формы, переадресация на страницу с которой пришел пользователь, или страницу логина

        """
        self.blog = Blog.objects.get(pk=self.kwargs['pk'])
        if self.blog.user == request.user or request.user.is_superuser:
            self.form = BlogForm(request.POST, instance=self.blog)
            if self.form.is_valid():
                self.form.save()
                messages.add_message(request, messages.SUCCESS, 'Статья успешно изменена')
                redirect_url = reverse('blog_index') + '?page' + self.request.GET['page']
                try:
                    redirect_url = redirect_url + '&search=' + self.request.GET['search']
                except KeyError:
                    pass
                try:
                    redirect_url = redirect_url + '&tag=' + self.request.GET['tag']
                except KeyError:
                    pass
                return redirect(redirect_url)
            else:
                return super(BlogUpdate, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))
