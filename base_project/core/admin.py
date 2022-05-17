from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from base_project.core import models


@admin.action(description=_('soft delete'))
def soft_delete(_, __, queryset):
    return queryset.soft_delete()


@admin.action(description=_('restore'))
def restore(_, __, queryset):
    return queryset.restore()


class UndeletableSelectedMixin:

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, *args, **kwargs):
        return False


class SoftDeletableSelectedMixin:

    def get_actions(self, request):
        self.actions += [soft_delete, restore]
        return super().get_actions(request)

    @admin.display(description=_('active'))
    def is_active(self, obj):
        color = 'red' if obj.is_deleted else 'green'
        mark = '×' if obj.is_deleted else '✓'
        return mark_safe(f'<span style="color: {color};">{mark}</span>')


class UneditableSelectedMixin:

    def has_change_permission(self, *args, **kwargs):
        return False
