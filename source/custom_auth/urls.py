from django.urls import path
import django_cas_ng.views as cas_views

from . import views

urlpatterns = [
    path('login/', views.login, name='cas_ng_login'),
    path('logout/', cas_views.LogoutView.as_view(), name='cas_ng_logout'),
    path('callback/', cas_views.CallbackView.as_view(), name='cas_ng_proxy_callback'),
    path('home/', views.home, name='home'),
]