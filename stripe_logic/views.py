import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View

from core_files.settings import DOMAIN_NAME, STRIPE_PUBLIC_KEY
from .models import Item
from django.views.generic import DetailView, TemplateView


stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemView(DetailView):
    model = Item
    template_name = "stripe_logic/item_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": STRIPE_PUBLIC_KEY
        })
        return context


class BuyItemView(View):
    def get(self, request, *args, **kwargs):
        item = Item.objects.get(id=self.kwargs.get('pk'))
        checkout_session = stripe.checkout.Session.create(
            metadata={
                "item_id": item.id
            },
            line_items=[
                {
                    'price_data': {
                        'currency': 'rub',
                        'unit_amount': int(item.price),
                        'product_data': {
                            'name': item.name
                        },
                    },
                    'quantity': 1,
                },
            ],
            payment_method_types=['card'],
            mode='payment',
            success_url=f'{DOMAIN_NAME}/success/',
            cancel_url=f'{DOMAIN_NAME}/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class SuccessView(TemplateView):
    template_name = "stripe_logic/success.html"


class CancelView(TemplateView):
    template_name = "stripe_logic/cancel.html"
