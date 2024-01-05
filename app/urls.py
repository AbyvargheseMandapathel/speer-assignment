from django.urls import path
from .views import NoteDetailView, NoteListCreateView, NoteSearchView, ShareNoteView, SharedNotesView, UserSignupView, UserLoginView

urlpatterns = [
    path('auth/signup', UserSignupView.as_view(), name='signup'),
    path('auth/login', UserLoginView.as_view(), name='login'),
    path('notes', NoteListCreateView.as_view(), name='notes'),
    path('notes/<int:pk>', NoteDetailView.as_view(), name='note-detail'),
    path('notes/<int:pk>/share/', ShareNoteView.as_view(), name='note-share'),
    path('shared-notes/', SharedNotesView.as_view(), name='shared-notes'),
    path('search/', NoteSearchView.as_view(), name='note-search'),

]