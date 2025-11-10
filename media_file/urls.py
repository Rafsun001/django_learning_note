
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app1/', include("app1.urls"))
]

########################################################
###################### Media File Handling #############
########################################################
"""  
Aita urlpatterns patterns er niche hubohu likhte hobe.
"""
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
##########