from django.urls import path
from .views import *

urlpatterns = [
    path("", index),
    path("resources", WarehouseStocksView.as_view()),
    path("total_cost", total_cost, name="total_cost")
]

