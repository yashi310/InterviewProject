from django.urls import path
from . import views
from .views import InterviewCreate,DeleteView,Update,ParticipantRegister
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', InterviewCreate.as_view(), name='interview-create'),
    path('member-create', ParticipantRegister.as_view(), name='member-create'),
    path('interview-delete/<int:pk>/',DeleteView.as_view(),name='interview-delete'),
    path('interview-update/<int:pk>/',Update.as_view(),name='interview-update'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
