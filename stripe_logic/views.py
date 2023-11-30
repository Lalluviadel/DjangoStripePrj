import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import DetailView, TemplateView

from core_files.settings import DOMAIN_NAME, STRIPE_PUBLIC_KEY, STRIPE_ENDPOINT_SECRET
from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_striped_price(float_val):
    return int(float_val) * 100

def get_tax(tax_obj):
    tax = stripe.TaxRate.create(
        display_name=tax_obj.name,
        inclusive=False,
        percentage=tax_obj.value,
        country='PL',
        description=tax_obj.name,
    )
    return str(tax.id)

def get_coupon(discount_obj):
    coupon = stripe.Coupon.create(
        percent_off=discount_obj.value,
        duration="once",
    )
    return str(coupon.id)


class ItemView(DetailView):
    model = Item
    template_name = "stripe_logic/item_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": STRIPE_PUBLIC_KEY
        })
        return context


class OrderView(DetailView):
    model = Order
    template_name = "stripe_logic/order_detail.html"

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
    def get(self, request, *args, **kwargs):
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
            discounts=[{"coupon": get_coupon(order.discount)}],
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


class WebhookView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        endpoint_secret = STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
            session = stripe.checkout.Session.retrieve(event['data']['object']['id'])
            order = Order.objects.get(id=int(session.metadata.order_id))
            if event['type'] == 'checkout.session.completed':
                order.status = Order.PAID
                order.save()
            elif event['type'] == 'checkout.session.async_payment_failed':
                order.status = Order.FAILED
                order.save()
        except (ValueError, AttributeError):
            return HttpResponse(status=400)
        except (stripe.error.SignatureVerificationError, stripe.error.InvalidRequestError):
            return HttpResponse(status=400)
        return HttpResponse(status=200)
