from django.urls import path

from auth.views import LogInView

urlpatterns = [
    path('login/', LogInView.as_view(), name='login')
]
