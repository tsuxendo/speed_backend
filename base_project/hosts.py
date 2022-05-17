from django_hosts import patterns, host


host_patterns = patterns('',
    host(r'admin', 'base_project.urls', name='admin'),
    host(r'api', 'base_project.rest_api.urls', name='rest_api'),
)
