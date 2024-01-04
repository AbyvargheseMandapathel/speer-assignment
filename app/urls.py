from django.urls import path
from .views import UserSignupView, UserLoginView

urlpatterns = [
    path('auth/signup', UserSignupView.as_view(), name='signup'),
    path('auth/login', UserLoginView.as_view(), name='login'),
]