from django.urls import path
from . import views

urlpatterns = [
    path('kk/', views.candlestick_chart, name='candlestick-chart'),
]
