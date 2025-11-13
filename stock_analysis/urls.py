from django.urls import path
from . import views

urlpatterns = [
    path("stocks/", views.stocks, name="stocks"),
    path(
        "stock_autocomplete/",
        views.StockAutoComplete.as_view(),
        name="stock_autocomplete",
    ),
    path("stock_detail/<int:pk>/", views.stock_detail, name="stock_detail"),  # type: ignore
]
