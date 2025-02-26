from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import CustomUser
from api.serializers import RegisterSerializer, LoginSerializer
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# API: Register New User
class RegisterView(generics.CreateAPIView):
    """
    API view for registering a new user.
    """
    queryset = CustomUser.objects.all()  # Queryset of all CustomUser objects
    permission_classes = [AllowAny]  # Allows anyone to access this view
    serializer_class = RegisterSerializer  # Serializer for validating and creating user data

# API: Login User
class LoginView(APIView):
    """
    API view for user login.
    """
    permission_classes = [AllowAny]  # Allows anyone to access this view

    def post(self, request):
        """
        Handles POST requests for user login.
        """
        serializer = LoginSerializer(data=request.data)  # Serializes the request data using LoginSerializer
        if serializer.is_valid():  # Checks if the serialized data is valid
            email = serializer.validated_data["email"]  # Extracts the email from the validated data
            password = serializer.validated_data["password"]  # Extracts the password from the validated data
            user = authenticate(email=email, password=password)  # Authenticates the user using email and password

            if user:  # Checks if the user is authenticated
                refresh = RefreshToken.for_user(user)  # Generates a refresh token for the authenticated user
                return Response({
                    "refresh": str(refresh),  # Returns the refresh token as a string
                    "access": str(refresh.access_token),  # Returns the access token as a string
                    "message": "Login successful"  # Returns a success message
                }, status=status.HTTP_200_OK)  # Returns a 200 OK status

            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)  # Returns a 401 Unauthorized status if authentication fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Returns a 400 Bad Request status if the serialized data is invalid

# API: Logout User
class LogoutView(APIView):
    """
    API view for user logout.
    """
    permission_classes = [IsAuthenticated]  # Requires the user to be authenticated to access this view
    @method_decorator(csrf_exempt)  # Disable CSRF for this API
    def dispatch(self, *args, **kwargs):
        """
        Dispatches the request after disabling CSRF.
        """
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        """
        Handles POST requests for user logout.
        """
        try:
            refresh_token = request.data["refresh"]  # Extracts the refresh token from the request data
            token = RefreshToken(refresh_token)  # Creates a RefreshToken object from the refresh token string
            token.blacklist()  # Blacklists the refresh token, effectively logging the user out
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)  # Returns a 205 Reset Content status with a success message
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)  # Returns a 400 Bad Request status if the token is invalid