from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from chat.views import IndexView, Register, Logout, LoginView, AfterLogin, NotFoundView, ExistsView, MessageView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', IndexView.as_view()),
    url(r'^sign_up/$', Register.as_view()),
    url(r'^log_out/$', Logout.as_view()),
    url(r'^log_in/$', LoginView.as_view()),
    url('not_found/', NotFoundView.as_view()),
    url('loged_in/', AfterLogin.as_view()),
    url('exists/', ExistsView.as_view()),
    url(r'^submit/$', MessageView.as_view()),

]