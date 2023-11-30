"""Contains views for working with objects of items, orders and stripe API."""

from core_files.settings import (
    DOMAIN_NAME,
    STRIPE_ENDPOINT_SECRET,
    STRIPE_PUBLIC_KEY
)

from django.conf import settings
from django.http import (HttpResponse, JsonResponse)
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView

import stripe

from .mixins import TitleMixin
from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_striped_price(float_val):
    """Return the item price value in the correct format."""
    return int(float_val) * 100


def get_tax(tax_obj):
    """Create TexRate and return its id."""
    tax = stripe.TaxRate.create(
        display_name=tax_obj.name,
        inclusive=False,
        percentage=tax_obj.value,
        country='PL',
        description=tax_obj.name,
    )
    return tax.id


def get_coupon(discount_obj):
    """Create Coupon and return its id."""
    coupon = stripe.Coupon.create(
        percent_off=discount_obj.value,
        duration='once',
    )
    return coupon.id


class ItemView(DetailView, TitleMixin):
    """View for a specific Item."""

    model = Item
    template_name = 'stripe_logic/item_detail.html'
    title = 'Buy this cool item!'

    def get_context_data(self, **kwargs):
        """Update context with stripe public key."""
        context = super().get_context_data(**kwargs)
        context.update({
            'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY
        })
        return context


class OrderView(DetailView):
    """View for a specific order."""

    model = Order
    template_name = 'stripe_logic/order_detail.html'
    title = 'Pay for the order'

    def get_context_data(self, **kwargs):
        """Update context with stripe public key."""
        context = super().get_context_data(**kwargs)
        context.update({
            'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY
        })
        return context


class BuyItemView(View):
    """View to Stripe Checkout Session create and buy items."""

    def get(self, request, *args, **kwargs):
        """Stripe Checkout Session create and buy items."""
        item = Item.objects.get(id=self.kwargs.get('pk'))
        checkout_session = stripe.checkout.Session.create(
            metadata={
                'item_id': item.id
            },
            line_items=[
                {
                    'price_data': {
                        'currency': 'rub',
                        'unit_amount': get_striped_price(item.price),
                        'product_data': {
                            'name': item.name
                        },
                    },
                    'quantity': item.quantity,
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


class BuyOrderView(View):
    """View to Stripe Checkout Session create and pay orders."""

    def get(self, request, *args, **kwargs):
        """Stripe Checkout Session create and pay orders."""
        order = Order.objects.get(id=self.kwargs.get('pk'))
        tax = order.tax
        order_items = [
            {
                'price_data': {
                    'currency': 'rub',
                    'unit_amount': get_striped_price(item.price),
                    'product_data': {
                        'name': item.name
                    },
                },
                'quantity': item.quantity,
                'tax_rates': [get_tax(tax)],
            } for item in order.get_items()
        ]
        checkout_session = stripe.checkout.Session.create(
            metadata={
                'order_id': order.id
            },
            line_items=order_items,
            discounts=[{'coupon': get_coupon(order.discount)}],
            payment_method_types=['card'],
            mode='payment',
            success_url=f'{DOMAIN_NAME}/success/',
            cancel_url=f'{DOMAIN_NAME}/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class SuccessView(TemplateView):
    """Success payment view."""

    template_name = 'stripe_logic/success.html'


class CancelView(TemplateView):
    """View if the payment has been cancelled."""

    template_name = 'stripe_logic/cancel.html'


class WebhookView(View):
    """Order change status webhook view."""

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """Solve problems with CSRF and class views."""
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Track the payment result and change the order status."""
        endpoint_secret = STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
            session = stripe.checkout.Session.retrieve(
                event['data']['object']['id']
            )
            order = Order.objects.get(id=int(session.metadata.order_id))
            if event['type'] == 'checkout.session.completed':
                order.status = Order.PAID
                order.save()
            elif event['type'] == 'checkout.session.async_payment_failed':
                order.status = Order.FAILED
                order.save()
        except (ValueError, AttributeError):
            return HttpResponse(status=400)
        except (stripe.error.SignatureVerificationError,
                stripe.error.InvalidRequestError):
            return HttpResponse(status=400)
        return HttpResponse(status=200)
