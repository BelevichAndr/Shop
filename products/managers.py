from django.db.models import Manager, QuerySet


class PublishedManager(Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class BasketQuerySet(QuerySet):

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def total_sum(self):
        return sum(basket.sum() for basket in self)
