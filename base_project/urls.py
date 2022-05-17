from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


admin.site.site_header = ''

admin.site.site_title = ''

admin.site.index_title = ''

admin.site.site_url = ''

admin.site.enable_nav_sidebar = True


urlpatterns = [
    path('', admin.site.urls)
]
