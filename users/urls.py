from django.urls import path

from products.views import RegisterClientView

urlpatterns = [
    path('client-registration/', RegisterClientView.as_view(), name='client_registration'),
]
