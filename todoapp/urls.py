from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('tasks.urls', namespace="tasks")),
    path('admin/', admin.site.urls),
]

if not settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns
