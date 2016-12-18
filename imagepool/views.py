from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
import json
from imagepool.models import ImagePool


def get_list(request):
    """ Контроллер возвращает список изображений в хранилище"""
    try:
        page_num = request.GET['page']
    except KeyError:
        page_num = '1'
    paginator = Paginator(ImagePool.objects.filter(user=request.user), 4)
    try:
        page = paginator.page(page_num)
    except InvalidPage:
        page = paginator.page(1)

    # Объявление переменных контекста
    # для преобразования в json
    output = dict()
    output['images'] = list()

    # images - список словарей
    # где src - ссылка на изображение
    # delete_src - ссылка на удаление изображения
    for image in page:
        output['images'] = output['images'] + [{'src': image.image.url,
                                                'delete_src': reverse('imagepool_delete',
                                                kwargs={'pk': image.pk})}]

    # Формирование урлов для навигации по страницам
    if page.has_previous():
        output['prev_url'] = reverse('imagepool_index') + '?page=' + str(page.previous_page_number())
    else:
        output['prev_url'] = ''
    if page.has_next():
        output['next_url'] = reverse('imagepool_index') + '?page=' + str(page.next_page_number())
    else:
        output['next_url'] = ''
    return HttpResponse(json.dumps(output), content_type='application/json')


def upload_file(request):
    """ Контроллер для загрузки файла в хранилище """
    if request.method == "POST":
        if request.FILES['file_to_upload']:
            image = ImagePool(user=request.user,
                              image=request.FILES['file_to_upload'])
            image.save()
            return HttpResponse('!!!')
        else:
            return HttpResponse("!!!")
    else:
        return HttpResponse("!!!")


def delete_file(request, pk):
    """ Контроллер для удаления файла из хранилища """
    try:
        ImagePool.objects.get(pk=pk).delete()
    except ImagePool.DoesNotExist:
        pass
    return HttpResponse(json.dumps({'status': 1}),
                        content_type='application/json')