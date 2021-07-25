from django.urls import path
from .views import DashboardView, CatalogView, get_data, snapshot_ready, shopify_orders_data, \
    import_csv, get_sku_data, ImportA2000View, upload_a2000, import_a2000, sku_inventory_change, \
    create_callback

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('catalog/', CatalogView.as_view(), name="catalog"),
    path('import_a2000/', ImportA2000View.as_view(), name='import_a2000_view'),
    path('get_order_data/', shopify_orders_data),
    path('get_sku_data/', get_sku_data),
    path('get_data/', get_data),
    path('snapshot_ready/', snapshot_ready),
    path('sku_inventory_change/', sku_inventory_change),
    path('create_callback/', create_callback),
    path('import_csv/', import_csv),
    path('upload_a2000/', upload_a2000, name='upload_a2000'),
    path('calc_a2000/', import_a2000, name='import_a2000'),
]