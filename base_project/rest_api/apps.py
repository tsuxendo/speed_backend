from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RestApiConfig(AppConfig):
    name = 'base_project.rest_api'
    verbose_name = _('rest api')
