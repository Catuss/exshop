from django.conf.urls import url
from guestbook.views import GuestBookView

urlpatterns = [
    url(r'^$', GuestBookView.as_view(), name='guestbook'),
]