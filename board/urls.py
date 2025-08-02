# board/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Example: /board/1/
    path('board/<int:board_id>/', views.board_view, name='board_view'),
]