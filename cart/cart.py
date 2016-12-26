import random
from django.shortcuts import get_object_or_404
from cart.models import CartItem
from catalog.models import Good

CART_ID_SESSION_KEY = 'cart_id'

def _cart_id(request):
    """
    Если у пользователя нет сессии 'cart_id' - создает ее.
    Иначе - возвращает существующую.
    """
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():
    """ Генерация значения для айди сессии """
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*() '
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters)-1)]
    return cart_id

def get_cart_items(request):
    """ Возвращает предметы в корзине """
    return CartItem.objects.filter(cart_id=_cart_id(request))

def add_to_cart(request):
    """ Добавляет объект в корзину """
    good_pk = request.POST.get('good_pk', '')
    quantity = request.POST.get('quantity', 1)
    good = get_object_or_404(Good, pk=good_pk)
    goods_in_cart = get_cart_items(request)
    in_cart = False
    for good_item in goods_in_cart:                 # если объект есть в корзине, увеличивает его колличество
        if good_item.good.id == good.id:            # иначе - добавляет его в корзину.
            good_item.augment_quantity(quantity)
            in_cart = True
    if not in_cart:
        ci = CartItem()
        ci.good = good
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.save()

def cart_distinct_item_count(request):
    """ Возвращает колличество объектов в корзине """
    return get_cart_items(request).count()

def get_single_item(request, item_id):
    """
     Принимает обязательный аргумент - айди объекта.
     Возвращает этот объект, или ошибку 404
    """
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))

def update_cart(request):
    """
      Изменяет колличество объектов в корзине, или удаляет объект из корзины
    """
    good_pk = request.POST.get('good_pk')
    quantity = request.POST.get('quantity')
    cart_item = get_single_item(request, good_pk)
    if cart_item:
        if int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            remove_from_cart(request)

def remove_from_cart(request):
    """ Удаляет объект из корзины """
    item_id = request.POST.get('item_id')
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()

def is_empty(request):
    """ Возаращает True, если корзина пуста """
    return cart_distinct_item_count(request) == 0

def empty_cart(request):
    """ Очищает корзину """
    user_cart = get_cart_items(request)
    user_cart.delete()
