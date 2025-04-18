from django.urls import path

from users.views import RegisterClientView, GetAuthenticatedUserView

urlpatterns = [
    path('client-registration/', RegisterClientView.as_view(), name='client_registration'),
    path('authenticated/', GetAuthenticatedUserView.as_view(), name='authenticated')
]
