from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic.base import RedirectView

from .views import LoginView

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(next_page="/login"), name='logout')
]