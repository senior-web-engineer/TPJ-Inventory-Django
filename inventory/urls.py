from django.urls import path
from .views import GetToken, get_data, snapshot_ready, shopify_orders_data

urlpatterns = [
    path('token/', GetToken.as_view()),
    path('', shopify_orders_data),
    path('snapshotReady/', snapshot_ready),
    path('snapshot_ready/', snapshot_ready),
]