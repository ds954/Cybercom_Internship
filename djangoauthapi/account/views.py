from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser,Book,BorrowRequest
from .serializers import *
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.renderers import TemplateHTMLRenderer

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
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'register.html'

    def get(self, request):
        return Response({'serializer': RegisterSerializer()})  # Pass an empty serializer for the form


    def post(self,request):
        serializer_class = RegisterSerializer(data=request.data)  # Serializer for validating and creating user data
        if serializer_class.is_valid(raise_exception=True):
            user=serializer_class.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'registration successfull'}, template_name='register_success.html', status=status.HTTP_201_CREATED)
        return Response({'serializer': serializer_class}, template_name='register.html', status=status.HTTP_400_BAD_REQUEST)

   
# API: Login User
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    API view for user login.
    """
    permission_classes = [AllowAny] 
    renderer_classes=[TemplateHTMLRenderer]
    template_name='login.html'
    def get(self,request):
        return Response({"serializer":LoginSerializer})

    def post(self, request):
        """
        Handles POST requests for user login.
        """
        print("Received POST request:", request.data)
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
                # context = {
                #     'message': 'Login successful!',
                #     'refresh_token': token['refresh'],
                #     'access_token': token['access']
                # }
                # # Store tokens in session if needed
                # request.session['access_token'] = token['access']
                # request.session['refresh_token'] = token['refresh']
                # print(token)
                # return redirect('dashboard')

                # return Response({"context":context},template_name='dashboard.html')

            # return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)  # Returns a 401 Unauthorized status if authentication fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Returns a 400 Bad Request status if the serialized data is invalid


        
class profileview(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    Permission_classes=[IsAuthenticated]
    template_name = 'profile.html'
    def get(self,request):
        serializer_class = RegisterSerializer(request.user)  # Serializer for validating and creating user data
        # return Response(serializer_class.data)
        return Response(serializer_class.data)
    
    def post(self, request):
        user = request.user
        user.username = request.data.get("name", user.username)
        user.save()
        return redirect('profile')
    
class ChangePasswordView(APIView):
    # permission_classes = [IsAuthenticated]  # Requires the user to be authenticated to access this view
    def get(self, request):
        return render(request, 'change_password.html')

    # def post(self, request):
    #     serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user}) # Pass the user object
    #     if serializer.is_valid():
    #         return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        print("User:", request.user)  # Debugging
        print("Is authenticated:", request.user.is_authenticated)
        # if not request.user.is_authenticated:
        #     return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResetEmailView(APIView):
    def get(self, request):
        return render(request, 'reset_password.html')
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):

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
    # permission_classes = [IsAuthenticated]
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'update_profile.html'

    # def get(self, request):
    #     serializer = UpdateProfileSerializer(instance=request.user)
    #     return Response({'serializer': serializer})

    # def post(self, request):
    #     serializer = UpdateProfileSerializer(instance=request.user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return redirect('dashboard')  # Redirect to dashboard after updating profile
    #     return Response({'serializer': serializer}, template_name='update_profile.html', status=status.HTTP_400_BAD_REQUEST)
    
class DashboardView(APIView):
    # permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard.html'

    def get(self, request):
        books = Book.objects.all()
        book_serializer = BookSerializer(books, many=True)
        context = {
            'user': request.user,
            'books': books
        }
        return Response(context)
    
class BookView(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'dashboard.html'

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BorrowRequestView(APIView):
    # permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     """Create a borrow request."""
    #     serializer = BorrowRequestSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response({"message": "Borrow request submitted"}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk):
    #     """Update borrow request status."""
    #     borrow_request = get_object_or_404(BorrowRequest, id=pk)
    #     if "status" in request.data:
    #         borrow_request.status = request.data["status"]

    #         # If the request is accepted, mark the book as unavailable
    #         if borrow_request.status == "accepted":
    #             borrow_request.book.is_available = False
    #             borrow_request.book.save()

    #         # If the book is returned, mark it as available
    #         elif borrow_request.status == "book_returned":
    #             borrow_request.book.is_available = True
    #             borrow_request.book.save()

    #         borrow_request.save()
    #         return Response({"message": "Request updated successfully"}, status=status.HTTP_200_OK)

    #     return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            if book.is_available:
                book.is_available = False
                book.save()
                return redirect('dashboard')  # Redirect to dashboard after borrowing
            return Response({'message': 'Book is not available'}, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({'message': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
class CancelBorrowRequestView(generics.UpdateAPIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        borrow_request = get_object_or_404(BorrowRequest, id=self.kwargs['pk'], user=request.user)
        borrow_request.status = 'Cancel_Request'
        borrow_request.save()
        return Response({'message': 'Borrow request cancelled successfully'}, status=status.HTTP_200_OK)


# Return Book Request
class ReturnBookView(generics.UpdateAPIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        borrow_request = get_object_or_404(BorrowRequest, id=self.kwargs['pk'], user=request.user)
        borrow_request.status = 'book_returned'
        borrow_request.book.is_available = True
        borrow_request.book.save()
        borrow_request.save()
        return Response({'message': 'Book return request processed'}, status=status.HTTP_200_OK)