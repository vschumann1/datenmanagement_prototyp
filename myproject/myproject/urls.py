from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),  # Include your app's URLs
    path("select2/", include("django_select2.urls")),
    path('', RedirectView.as_view(url='/myapp/password/', permanent=True)),  # Redirect root URL to the password page
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
