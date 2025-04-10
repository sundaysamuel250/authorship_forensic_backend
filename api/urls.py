# api/urls.py

from django.urls import path
from .views import AnalyzeTextView  # make sure this exists

urlpatterns = [
    # Example URL route
    # path('views/', views.example_view, name='views'),
    path("analyze/", AnalyzeTextView.as_view(), name="analyze-text"),
]
