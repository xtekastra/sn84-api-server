from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("predict", views.predict, name="predict"),
    path('item_list/', views.item_list, name='history-list'),
    path('history/<int:pk>/', views.history_detail, name='history-detail'),
    path('rerun', views.rerun, name='rerun'),
]
