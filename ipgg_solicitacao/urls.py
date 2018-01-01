from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

handler404 = 'solicitacao.views.index'
handler500 = 'solicitacao.views.index'

urlpatterns = [
    url('admin/', admin.site.urls),
    url('solicitacao/', include('solicitacao.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

