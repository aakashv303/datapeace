from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('users/', views.UserList),
    path('users/<int:pk>/', views.UserDetail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
