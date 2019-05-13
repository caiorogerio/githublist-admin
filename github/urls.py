from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .api import LanguageListView, LanguageDetailView

app_name = 'github'

urlpatterns = format_suffix_patterns([
    path('languages/', LanguageListView.as_view(), name='language-list'),
    path('languages/<slug>/', LanguageDetailView.as_view(), name='language-detail'),
])
