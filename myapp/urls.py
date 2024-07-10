from django.urls import path
from . import views
from .views import password_protect

app_name = 'myapp'

urlpatterns = [
    path('', password_protect, name='home'),  # Leitet auf die Passwort-Seite
    path('password/', password_protect, name='password_protect'),
    path('main/', views.main_view, name='main_view'),
    path('prototyp/', views.hlk_view, name='hlk_view'),
    path('geo/', views.geo_view, name='geo_view'),
    path('personenbahn/', views.pb_view, name='pb_view'),
    path('personenbahn/<int:station_number>/', views.station_detail, name='pb_detail'),
    path('analysis_startseite/', views.analysis_startseite, name='analysis_startseite'),
    path('streckeninfo/', views.streckeninfo, name='streckeninfo'),
    path('sml/', views.sml_view, name='sml_view'),
    path('anlagen/<str:anlage_type>/', views.anlagen_view, name='anlagen'),
    path('etcs/', views.etcs_view, name='etcs_view'),
    path('elektr/', views.elektr_view, name='elektr_view'),
]
