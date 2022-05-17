from django.db.models.query import QuerySet
from django.utils.timezone import now


class SoftDeletionQuerySet(QuerySet):

    def soft_delete(self):
        return super().update(deleted_at=now())

    def restore(self):
        return super().update(deleted_at=None)

    def alived(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)
