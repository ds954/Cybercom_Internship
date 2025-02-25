from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .serializers import apiSerializer
from .models import apimodel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password

class ApiViewset(viewsets.ModelViewSet):
    """
    A ViewSet for handling CRUD (Create, Read, Update, Delete) operations on the apimodel.
    """
    queryset = apimodel.objects.all()
    serializer_class = apiSerializer

    @action(detail=False, methods=['post'])
    def add_user(self, request):
        """
        API endpoint to add a new user to the database.
        Accepts POST requests with user data and saves it if valid.
        Returns a 201 Created status if successful, otherwise 400 Bad Request.
        """
        serializer = apiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'put', 'delete'])
    def user_detail(self, request, pk=None):
        """
        Handles retrieving, updating, or deleting a specific user.
        - GET: Retrieves user details.
        - PUT: Updates user information.
        - DELETE: Removes the user from the database.
        """
        user = get_object_or_404(apimodel, pk=pk)

        if request.method == 'GET':
            serializer = apiSerializer(user)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = apiSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

def home(request):
    """
    Renders the home page with a list of users retrieved from the API.
    Fetches user data from the API endpoint and passes it to 'home.html'.
    """
    # API request to get user data
    response = requests.get('http://127.0.0.1:8000/user/')
    data = response.json()
    return render(request, 'home.html', {'data': data})

class UserRegistrationView(APIView):
    """
    API view for handling user registration.
    Accepts POST requests with user data and registers the user if valid.
    """

    def get(self, request):
        """
        Renders the registration page.
        """
        return render(request, 'register.html')

    def post(self, request):
        """
        Handles user registration.
        If the provided data is valid, a new user is created.
        Returns the created user data with a 201 status.
        Otherwise, returns validation errors with a 400 status.
        """
        serializer = apiSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = apiSerializer(user).data  # Serialize the user object
            return Response(user_data, status=status.HTTP_201_CREATED)  # Return the user data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """
    API view for handling user login.
    Accepts POST requests with username and password, authenticates the user,
    and redirects to the home page if successful.
    """

    def get(self, request):
        """
        Renders the login page.
        """
        return render(request, 'login.html')

    def post(self, request):
        """
        Handles user authentication.
        - If valid, logs in the user and redirects to 'home'.
        - If invalid, returns an error message with status 401 (Unauthorized).
        """
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate using Django's built-in authentication system
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after login
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    """
    API view for handling user logout.
    Logs out the user and redirects to the login page.
    """

    def get(self, request):
        """
        Handles user logout and redirects to login page.
        """
        logout(request)
        return redirect('login')

def home(request):
    """
    Renders the home page with all user data from the apimodel.
    Fetches all records from the apimodel and passes them to 'home.html'.
    """
    data = apimodel.objects.all()
    return render(request, 'home.html', {'data': data})