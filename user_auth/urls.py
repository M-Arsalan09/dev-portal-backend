from django.urls import path
from .views import LoginView, UpdatePasswordView, CreateUserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('update-password/', UpdatePasswordView.as_view(), name='update_password'),
    path('create-user/', CreateUserView.as_view(), name='create_user'),
]