from django.db.models import Manager, QuerySet


class PublishedManager(Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class BasketQuerySet(QuerySet):

    def get_total_quantity(self):
        return sum(basket.quantity for basket in self)

    def get_total_sum(self):
        return sum(basket.get_object_sum() for basket in self)

    def get_stripe_products(self):
        item_list = []
        for basket in self:
            item = {
                "price": basket.product.stripe_product_price_id,
                "quantity": basket.quantity
            }
            item_list.append(item)

        return item_list
