from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, registerSerializer
from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets, filters
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_str
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

# API to reset user's password using unique token and user ID
class ResetPasswordView(APIView):
    """
    Resets the user's password.
    """
    # Handles POST request to reset password
    def post(self, request, *args, **kwargs):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('newPassword')

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid token or user ID"}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


# API to send password reset email to user
class ForgotPasswordView(APIView):
    # Handles POST request to send reset email
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                # Generate a one-time use token and UID
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # Create reset password URL
                reset_url = f'http://localhost:8000/accounts/reset_page/?uid={uid}&token={token}'
                # Send email
                send_mail(
                    'Password Reset Request',
                    f'Please follow the link to reset your password: {reset_url}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                pass # Silently ignore invalid email requests
        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


# API to create a new user account
class UserCreate(APIView):
    """
    Creates the user.
    """
    # Handles POST request to create user
    def post(self, request, format='json'):
        serializer = registerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Function to log out the user
@require_POST  
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True}, status=200)

# API to get total number of categories
@api_view(['GET'])
def total_categories(request):
    count = Category.objects.count()
    return Response({'total_categories': count})

# API to get total number of items
@api_view(['GET'])
def total_items(request):
    count = Item.objects.count()
    return Response({'total_items': count})

# ViewSet for Item model with CRUD operations, filtering, and sorting
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'tags']  # Add the fields you want to filter by
    ordering_fields = ['name', 'sku', 'in_stock', 'available_stock']  # Add the fields you want to be sortable by

    def get_queryset(self):
        queryset = Item.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query is not None:
            queryset = queryset.filter(
                Q(sku__icontains=search_query) | 
                Q(name__icontains=search_query) |
                Q(tags__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        return queryset
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'error': 'An Item with this SKU already exists.'}, status=status.HTTP_400_BAD_REQUEST)

# ViewSet for Category model with CRUD operations
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'error': 'A category with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

# Renders login page, ensuring it's never cached
@never_cache
def login_page(request):
    context = {
        'api_key': settings.API_KEY, 
    }
    return render(request, 'login.html', context)

# Renders root page, ensuring it's never cached
@never_cache
def root(request):
    context = {
        'api_key': settings.API_KEY,
    }
    return render(request, 'login.html',context)

# Renders dashboard page, ensuring it's never cached
@never_cache
def dashboard(request):
    context = {
        'api_key': settings.API_KEY,
    }
    return render(request, 'dashboard.html',context)

# Renders reset password page, ensuring it's never cached
def reset_page(request):
    context = {
        'api_key': settings.API_KEY, 
    }
    return render(request, 'reset_page.html', context)


# API for user login, returns auth token if successful
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Incorrect Credentials"}, status=status.HTTP_400_BAD_REQUEST)


