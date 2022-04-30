
from django.urls import path, include
from django.contrib import admin
# from django.contrib.auth import views as auth_views
from importexport import views as ieviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', ieviews.home, name='home'),
    path('importexport/', include('importexport.urls')),
]
