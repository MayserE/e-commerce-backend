from django.urls import path

from orders.views import GenerateOrderView, OrderListView, OrderDetailView

urlpatterns = [
    path('', GenerateOrderView.as_view(), name='generate_order'),
    path('list-user-order/', OrderListView.as_view(), name='list_user_order'),
    path('order-detail/<order_id>/', OrderDetailView.as_view(), name='order_detail'),
]
