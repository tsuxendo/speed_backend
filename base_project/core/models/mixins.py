import uuid

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from base_project.core.query import SoftDeletionQuerySet


class UUIDPrimaryKeyModelMixin(models.Model):
    """UUID Primary Key Model Mixin
    Set uuid field `id` as primary key field.
    """
    id = models.UUIDField(
        _('id'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class TimeStampModelMixin(models.Model):
    """Time Stamped Model Mixin
    Add `created_at` and `updated_at` fields.
    """
    created_at = models.DateTimeField(
        _('created datetime'),
        auto_now_add=True,
        # db_index=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        _('updated datetime'),
        auto_now=True,
        # db_index=True,
        editable=False,
    )

    class Meta:
        abstract = True
        ordering = ('-created_at', '-updated_at')


class SoftDeletionModelMixin(models.Model):
    """Soft Deletion Model Mixin
    Add soft deleted flag.
    """
    deleted_at = models.DateTimeField(
        _('deleted datetime'),
        blank=True,
        null=True,
        default=None,
        editable=False,
        # db_index=True,
    )

    objects = SoftDeletionQuerySet.as_manager()

    class Meta:
        abstract = True

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def soft_delete(self):
        self.deleted_at = now()
        return self.save()

    def restore(self):
        self.deleted_at = None
        return self.save()
