from django.contrib import admin
from django.urls import path
from stripe_logic.views import (
    BuyItemView,
    CancelView,
    ItemView,
    SuccessView, BuyOrderView, OrderView, WebhookView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buy/<pk>/', BuyItemView.as_view(), name='buy'),
    path('buy-order/<pk>/', BuyOrderView.as_view(), name='buy_order'),
    path('item/<pk>/', ItemView.as_view(), name='item_info'),
    path('order/<pk>/', OrderView.as_view(), name='order_info'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('webhook/', WebhookView.as_view(), name='webhook'),
]
