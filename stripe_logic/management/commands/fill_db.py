""" TODO: to the README.md: python manage.py fill_db
"""
import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from stripe_logic.models import Item

JSON_PATH = 'fixtures'


def load_from_json(file_name):
    with open(f'{JSON_PATH}/{file_name}', mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        Item.objects.all().delete()
        items = load_from_json('items.json')
        for item in items:
            raw_item_data = item.get('fields')
            raw_item_data['id'] = item.get('pk')
            new_item = Item(**raw_item_data)
            new_item.save()

        User.objects.create_superuser('admin', 'admin@testtest.ru', 'admin')
