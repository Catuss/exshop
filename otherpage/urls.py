from django.conf.urls import url
from otherpage.views import AboutView, ContactView, HowtobuyView


urlpatterns = [
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^contacts/$', ContactView.as_view(), name='contact'),
    url(r'^howtobuy/$', HowtobuyView.as_view(), name='howtobuy'),
]

