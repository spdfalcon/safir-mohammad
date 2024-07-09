from django.urls import re_path, path

from .views import manifest, service_worker, offline, assetlinks

# Serve up serviceworker.js and manifest.json at the root
urlpatterns = [
    re_path(r'^serviceworker\.js$', service_worker, name='serviceworker'),
    re_path(r'^manifest\.json$', manifest, name='manifest'),
    re_path('^offline/$', offline, name='offline'),
    path('.well-known/assetlinks.json/', assetlinks, name='assetlinks')
]
