from django.urls import include, path
from rest_framework import routers
from base_project.rest_api import views


router = routers.DefaultRouter()


# router.register('prefix', views.ViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
