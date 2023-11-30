"""Provides package integration into the admin panel."""
from django.contrib import admin
from .models import Item, Order

admin.site.register(Item)
admin.site.register(Order)
