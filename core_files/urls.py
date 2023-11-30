from django.contrib import admin
from django.urls import path
from stripe_logic.views import (
    BuyItemView,
    CancelView,
    ItemView,
    SuccessView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buy/<pk>/', BuyItemView.as_view(), name='buy'),
    path('item/<pk>/', ItemView.as_view(), name='item_info'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
]
