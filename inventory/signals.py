from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderProduct
import logging


@receiver(post_save, sender=Order)
def create_order_product(sender, instance, created, **kwargs):
    if created:
        # check if the Order instance has been saved
        if instance.pk:
            # create the related OrderProduct instance
            product = instance.products.first()  # get the first product in the order
            quantity = 1  # set the default quantity to 1
            OrderProduct.objects.create(order=instance, product=product, quantity=quantity)
        else:       
            # log an error message
            logger = logging.getLogger(__name__)
            logger.error('Order instance has not been saved yet')                     