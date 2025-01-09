from django.urls import path

from .views import PredictCreateView, PredictDetailView, PredictionDeleteView, PredictionHistoryView


app_name = 'core'

urlpatterns = [
    path('form/', PredictCreateView.as_view(), name='predict_form'),
    path('<int:pk>/', PredictDetailView.as_view(), name='predict_detail'),
    path('history/', PredictionHistoryView.as_view(), name='prediction_history'),
    path('delete/<int:pk>/', PredictionDeleteView.as_view(), name='prediction_delete'),
]
