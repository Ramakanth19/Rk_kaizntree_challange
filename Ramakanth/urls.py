from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # URL for Django's built-in admin interface.
    path('accounts/', include('accounts.urls')),  # Routes all 'accounts/' URLs to the accounts app.
    path('api/accounts/', include('accounts.urls')),  # Routes 'api/accounts/' URLs to the accounts app, potentially for API-related paths.
    path('api/', include('accounts.urls')),  # Redirects API root to accounts URLs, which might be an oversight or specific design choice.
    path('', include('accounts.urls')),  # Maps the root URL to accounts app, making it the default entry point for the web application.
]
