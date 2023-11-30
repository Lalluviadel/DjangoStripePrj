from django.core.validators import MaxValueValidator
from django.db import models


class Discount(models.Model):
    name = models.CharField(max_length=64, verbose_name='наименование',)
    value = models.PositiveIntegerField(verbose_name='размер скидки', default=10,
                                        validators=[MaxValueValidator(90),])

    def __str__(self):
        return f'{self.name} - {self.value}'


class Tax(models.Model):
    name = models.CharField(max_length=64, verbose_name='наименование',)
    value = models.PositiveIntegerField(verbose_name='размер налога', default=10,
                                        validators=[MaxValueValidator(50),])

    def __str__(self):
        return f'{self.name} - {self.value}'


class Order(models.Model):
    PAID = 'PD'
    PROCEEDED = 'PRD'
    FAILED = 'FLD'

    ORDER_STATUS_CHOICES = (
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (FAILED, 'проблема с оплатой'),
    )

    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='статус', max_length=3, default=PROCEEDED)
    discount = models.ForeignKey(Discount, blank=True, null=True, verbose_name='Скидка', on_delete=models.CASCADE)
    tax = models.ForeignKey(Tax, blank=True, null=True, verbose_name='Налог', on_delete=models.CASCADE)

    def __str__(self):
        return f'Заказ № {self.pk} {self.status}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_cost(), items)))

    def get_items(self):
        return self.orderitems.select_related()


class Item(models.Model):
    """The model for the order item."""
    name = models.CharField(max_length=64, verbose_name='наименование',)
    description = models.TextField(blank=True, verbose_name='описание',)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='стоимость',)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=1)
    order = models.ForeignKey(Order, verbose_name='заказ', related_name='orderitems', on_delete=models.CASCADE, default=1)

    def __str__(self):
        """Forms a printable representation of the object."""
        return self.name

    def get_price(self):
        return self.price

    def get_cost(self):
        return self.price * self.quantity
