"""gin_rummy_scoresheet URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),

    # API Documentation ()
    path('api-docs/', include_docs_urls(title='Gin Rummy Scoresheet API')),
    path('', include('frontend.urls')),
]
