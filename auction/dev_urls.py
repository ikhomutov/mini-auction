import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include, path

from .urls import urlpatterns

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
