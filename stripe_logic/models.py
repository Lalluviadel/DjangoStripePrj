from django.db import models


class Item(models.Model):
    """The model for the order item."""
    name = models.CharField(max_length=64, verbose_name='наименование',)
    description = models.TextField(blank=True, verbose_name='описание',)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='стоимость',)

    def __str__(self):
        """Forms a printable representation of the object."""
        return self.name

    def get_price(self):
        return self.price
