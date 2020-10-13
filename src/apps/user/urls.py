from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('users/', views.UsersView.as_view(), name='users'),
    path('users/<user_id>/', views.UserDetailsView.as_view(), name='user_details'),
]
