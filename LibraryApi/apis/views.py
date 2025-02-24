from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .serializers import apiSerializer
from .models import apimodel

class ApiViewset(viewsets.ModelViewSet):
    """
    A ViewSet for handling CRUD operations on the apimodel.
    """
    queryset = apimodel.objects.all()
    serializer_class = apiSerializer

    @action(detail=False, methods=['post'])
    def add_user(self, request):
        """
        Adds a new user to the database.
        Accepts POST requests with user data and saves it if valid.
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
        - GET: Retrieves the user details.
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
    Makes a GET request to the API endpoint and passes the data to 'home.html'.
    """
     # url= "https://newsapi.org/v2/everything?q=tesla&from=2025-01-24&sortBy=publishedAt&apiKey=ff87fcb3100549faa85f8228d95ef324"
    # response=requests.get(url)
    # data=response.json()
    # art=data['articles']
    response = requests.get('http://127.0.0.1:8000/user/')
    data = response.json()
    return render(request, 'home.html', {'data': data})

class UserRegistrationView(APIView):
    """
    API view for handling user registration.
    Accepts POST requests with user data and registers the user if valid.
    """
    def post(self, request):
        serializer = apiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
