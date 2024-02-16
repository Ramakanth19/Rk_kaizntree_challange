from django.conf import settings
from django.http import JsonResponse
from django.urls import resolve  # Used to match request path for exemptions

class APIKeyAuthenticationMiddleware:
    """
    Middleware to enforce API key authentication on all requests except for those to exempt paths.
    """
    def __init__(self, get_response):
        # Middleware initialization (Django standard procedure)
        self.get_response = get_response

    def __call__(self, request):
        # List of paths exempt from API key authentication. Adjust as necessary.
        exempt_paths = [
            '/',
            '/accounts/login_page/', 
            '/accounts/reset_page/',  # Paths where API key is not required.
            '/accounts/dashboard/',
        ]

        # Skip API key check for exempt paths
        if request.path not in exempt_paths:
            # Retrieve API key from request headers
            api_key_header = request.headers.get('X-API-KEY')
            # Validate API key; respond with error if invalid
            if api_key_header != settings.API_KEY:
                return JsonResponse({'error': 'Invalid API Key'}, status=401)

        # Proceed with request processing if API key is valid or not required
        response = self.get_response(request)
        return response

class NoCacheMiddleware:
    """
    Middleware to prevent caching of responses by setting appropriate headers.
    This ensures fresh server responses for every request.
    """
    def __init__(self, get_response):
        # Middleware initialization
        self.get_response = get_response

    def __call__(self, request):
        # Process the request and get the response
        response = self.get_response(request)
        # Set headers to prevent caching
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
