from django.urls import path
from .views import NoteDetailView, NoteListCreateView, UserSignupView, UserLoginView

urlpatterns = [
    path('auth/signup', UserSignupView.as_view(), name='signup'),
    path('auth/login', UserLoginView.as_view(), name='login'),
    path('notes', NoteListCreateView.as_view(), name='notes'),
    path('notes/<int:pk>', NoteDetailView.as_view(), name='note-detail'),

]