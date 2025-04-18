from django.urls import path

from categories.views import CreateCategoryView

urlpatterns = [
    path('', CreateCategoryView.as_view(), name='category_creation'),
]