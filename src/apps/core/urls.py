from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('server-info/', views.ServerInfoView.as_view(), name='server_info'),
]
