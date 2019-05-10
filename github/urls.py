from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .api import LanguageView, LanguageListSerializer, LanguageDetailSerializer

app_name = 'github'

urlpatterns = format_suffix_patterns([
    path('languages/', LanguageView.as_view(serializer_class=LanguageListSerializer), name='language-list'),
    path('languages/<int:pk>/', LanguageView.as_view(serializer_class=LanguageDetailSerializer), name='language-detail'),
])
