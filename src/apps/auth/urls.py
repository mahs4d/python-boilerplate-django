from django.urls import path
from . import views

app_name = 'auth'
urlpatterns = [
    path('auth/tokens/', views.TokensView.as_view(), name='tokens'),
    path('auth/otp-codes/', views.OtpCodeView.as_view(), name='otp_codes'),
    path('auth/roles/', views.RolesView.as_view(), name='roles'),
    path('auth/roles/<str:slug>/', views.RoleDetailsView.as_view(), name='role_details'),
]
