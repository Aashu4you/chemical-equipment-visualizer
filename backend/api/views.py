from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

def health_check(request):
    return JsonResponse({"status": "Backend is running"})

@api_view(['POST'])
def signup(request):
    name = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return JsonResponse(
            {"message": "Email and password are required"},
            status=400
        )

    if User.objects.filter(username=email).exists():
        return JsonResponse(
            {"message": "User already exists"},
            status=400
        )

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name=name or ""
    )

    token, _ = Token.objects.get_or_create(user=user)

    return JsonResponse({
        "token": token.key,
        "user": {
            "id": user.id,
            "name": user.first_name,
            "email": user.email
        }
    }, status=201)

@api_view(['POST'])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(username=email, password=password)

    if not user:
        return JsonResponse(
            {"message": "Invalid credentials"},
            status=401
        )

    token, _ = Token.objects.get_or_create(user=user)

    return JsonResponse({
        "token": token.key,
        "user": {
            "id": user.id,
            "name": user.first_name,
            "email": user.email
        }
    })
