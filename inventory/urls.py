from django.urls import path
from .views import DashboardView, CatalogView, get_data, snapshot_ready, shopify_orders_data, \
    import_csv

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('catalog/', CatalogView.as_view(), name="catalog"),
    path('order_data/', shopify_orders_data),
    path('get_data/', get_data),
    path('snapshot_ready/', snapshot_ready),
    path('import_csv/', import_csv),
]