from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser,Book,BorrowRequest
from .serializers import *
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
User = settings.AUTH_USER_MODEL



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# API: Register New User
class RegisterView(generics.CreateAPIView):
    """
    API view for registering a new user.
    """
    def post(self,request):
        serializer_class = RegisterSerializer(data=request.data)  # Serializer for validating and creating user data
        serializer_class.is_valid(raise_exception=True)
        user=serializer_class.save()
        token=get_tokens_for_user(user)
        return Response({'token':token,'msg':'registration successfull'})

   
# API: Login User
class LoginView(APIView):
    """
    API view for user login.
    """
    

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
                token=get_tokens_for_user(user)
                
                return Response({
                    "refresh": str(token),  # Returns the refresh token as a string
                    
                    "message": "Login successful"  # Returns a success message
                }, status=status.HTTP_200_OK)  # Returns a 200 OK status

            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)  # Returns a 401 Unauthorized status if authentication fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Returns a 400 Bad Request status if the serialized data is invalid

# # API: Logout User
# class LogoutView(APIView):
#     """
#     API view for user logout.
#     """
#     permission_classes = [IsAuthenticated]  # Requires the user to be authenticated to access this view
#     @method_decorator(csrf_exempt)  # Disable CSRF for this API
#     def dispatch(self, *args, **kwargs):
#         """
#         Dispatches the request after disabling CSRF.
#         """
#         return super().dispatch(*args, **kwargs)

#     def post(self, request):
#         """
#         Handles POST requests for user logout.
#         """
#         try:
#             refresh_token = request.data["refresh"]  # Extracts the refresh token from the request data
#             token = RefreshToken(refresh_token)  # Creates a RefreshToken object from the refresh token string
#             token.blacklist()  # Blacklists the refresh token, effectively logging the user out
#             return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)  # Returns a 205 Reset Content status with a success message
#         except Exception:
#             return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)  # Returns a 400 Bad Request status if the token is invalid
        
class profileview(APIView):
    def get(self,request):
        serializer_class = RegisterSerializer(request.user)  # Serializer for validating and creating user data
        Permission_classes=[IsAuthenticated]
        return Response(serializer_class.data)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]  # Requires the user to be authenticated to access this view
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user}) # Pass the user object
        if serializer.is_valid():
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
\

    def post(self, request, uid, token, format=None):
        serializer = PasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookView(APIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowRequestView(APIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer

    @action(detail=True,methods=['POST'])
    def accept(self,request,pk=None):
            borrow_request = get_object_or_404(BorrowRequest, id=pk)
            book = borrow_request.book
            book.is_available = False
            book.save()
            borrow_request.status = "accepted"
            borrow_request.save()

            return Response({"message": "Request accepted"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """ Reject a borrow request """
        borrow_request = get_object_or_404(BorrowRequest, id=pk)
        borrow_request.status = "rejected"
        borrow_request.save()

        return Response({"message": "Request rejected"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """ Cancel a borrow request """
        borrow_request = get_object_or_404(BorrowRequest, id=pk)
        borrow_request.status = "Cancel_Request"
        borrow_request.save()

        return Response({"message": "Request canceled"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """ Mark book as returned """
        borrow_request = get_object_or_404(BorrowRequest, id=pk)
        book = borrow_request.book
        book.is_available = True
        book.save()
        borrow_request.status = "book_returned"
        borrow_request.save()

        return Response({"message": "Book returned"}, status=status.HTTP_200_OK)