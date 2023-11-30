from django.urls import path
from .views import game_search_view

urlpatterns = [
    path('search/<str:game_name>/', game_search_view, name='game_search'),
]
