from django.conf.urls import include, url
from django.conf.urls import handler404
from colegio.views import mi_error_404
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import profiles.urls
import accounts.urls
import enrollment.urls
import register.urls
import income.urls
import cash.urls
import payments.urls
import discounts.urls
import AE_academico.urls
from . import views

handler404 = mi_error_404

urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r'^about/$', views.AboutPage.as_view(), name='about'),
    url(r'^users/', include(profiles.urls, namespace='profiles')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(accounts.urls, namespace='accounts')),
    url(r'^enrollments/', include(enrollment.urls, namespace='enrollments')),
    url(r'^registers/', include(register.urls, namespace='registers')),
    url(r'^cash/', include(cash.urls, namespace='cash')),
    url(r'^income/', include(income.urls, namespace='income')),
    url(r'^payments/', include(payments.urls, namespace='payments')),
    url(r'^discounts/', include(discounts.urls, namespace='discounts')),
    url(r'^academic/', include(AE_academico.urls, namespace='academic')),
]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
