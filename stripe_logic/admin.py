"""Provides package integration into the admin panel."""
from django.contrib import admin

from .models import Discount, Item, Order, Tax

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Discount)
admin.site.register(Tax)
