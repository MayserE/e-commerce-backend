from django.urls import path

from auth.view_profile import ProfileView
from auth.views import AuthView

urlpatterns = [
    path('login/', AuthView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
