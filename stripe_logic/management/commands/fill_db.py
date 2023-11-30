"""The command for filling the database."""
import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from stripe_logic.models import Discount, Item, Order, Tax

JSON_PATH = 'fixtures'


def load_from_json(file_name):
    """
    Load JSON file.

    Args:
        file_name (str): name of the JSON file.

    Returns:
        list: items data list.
    """
    with open(
            f'{JSON_PATH}/{file_name}', mode='r', encoding='utf-8'
    ) as infile:
        return json.load(infile)


class Command(BaseCommand):
    """The command for filling the database."""

    def handle(self, *args, **options):
        """Fill the database with Tax, Order, Discount, Item and User."""
        Tax.objects.all().delete()
        taxes = load_from_json('taxes.json')
        for tax in taxes:
            raw_tax_data = tax.get('fields')
            raw_tax_data['id'] = tax.get('pk')
            new_tax = Tax(**raw_tax_data)
            new_tax.save()

        Discount.objects.all().delete()
        discounts = load_from_json('discounts.json')
        for discount in discounts:
            raw_discount_data = discount.get('fields')
            raw_discount_data['id'] = discount.get('pk')
            new_discount = Discount(**raw_discount_data)
            new_discount.save()

        Order.objects.all().delete()
        orders = load_from_json('orders.json')
        for order in orders:
            raw_order_data = order.get('fields')
            raw_order_data['id'] = order.get('pk')
            if raw_order_data.get('tax'):
                _tax = Tax.objects.get(id=raw_order_data.get('tax'))
                raw_order_data['tax'] = _tax
            if raw_order_data.get('discount'):
                _discount = Discount.objects.get(
                    id=raw_order_data.get('discount')
                )
                raw_order_data['discount'] = _discount
            new_order = Order(**raw_order_data)
            new_order.save()

        Item.objects.all().delete()
        items = load_from_json('items.json')
        for item in items:
            raw_item_data = item.get('fields')
            _order = Order.objects.get(id=raw_item_data.get('order'))
            raw_item_data['order'] = _order
            raw_item_data['id'] = item.get('pk')
            new_item = Item(**raw_item_data)
            new_item.save()

        User.objects.all().delete()
        User.objects.create_superuser('admin', 'admin@testtest.ru', 'admin')
