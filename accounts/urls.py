from django.urls import path, include
from .api import login_page, LoginAPIView, dashboard, UserCreate, ForgotPasswordView, ResetPasswordView
from rest_framework.routers import DefaultRouter
from .api import ItemViewSet, CategoryViewSet, total_categories, total_items, logout_view, reset_page, root

# Initialize a DefaultRouter for REST Framework viewsets
router = DefaultRouter()
# Register Item and Category viewsets with the router for CRUD operations via API
router.register(r'items', ItemViewSet)
router.register(r'categories', CategoryViewSet)

# Define URL patterns for the app
urlpatterns = [
    path('', root, name='root'),  # The root page, often used for the app's main page or redirect
    path('login_page/', login_page, name='login-page'),  # Renders the login page
    path('login/', LoginAPIView.as_view(), name='login'),  # Endpoint for user login, returns a token upon success
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard page, typically requires user to be authenticated
    path('reset_page/', reset_page, name='reset_page'),  # Page where users can enter their new password
    path('total_categories/', total_categories, name='total-categories'),  # API endpoint to get the total number of categories
    path('total_items/', total_items, name='total-items'),  # API endpoint to get the total number of items
    path('', include(router.urls)),  # Includes the routes defined by the DefaultRouter for items and categories
    path('logout/', logout_view, name='logout'),  # Endpoint for logging out users, typically invalidates user's token
    path('register/', UserCreate.as_view(), name='account-create'),  # Endpoint for creating a new user account
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),  # Endpoint to initiate password reset via email
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),  # Endpoint to reset the user's password
]

