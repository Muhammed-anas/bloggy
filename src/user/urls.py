from django.urls import path

from .views import register_view, login_view, logout_user

urlpatterns = [
    path('register/',register_view.as_view(), name='register'),
    path('login/', login_view.as_view(), name='login'),
    path('logout/', logout_user, name='logout')
]

