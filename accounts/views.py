from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import UserInfo
from django.contrib.auth.hashers import make_password, check_password
from django.utils.timezone import now


# REGISTER VIEW
class RegisterView(APIView):
    def post(self, request):
        data = request.data

        user = UserInfo.objects.create(
            name=data.get("name"),
            email=data.get("email"),
            password=make_password(data.get("password")),
            role=data.get("role", "user")
        )

        return Response({
            "message": "User registered successfully",
            "user_id": user.user_id
        }, status=status.HTTP_201_CREATED)


# LOGIN VIEW
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = UserInfo.objects.get(email=email)
        except UserInfo.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)

        if not check_password(password, user.password):
            return Response({"error": "Invalid credentials"}, status=400)

        user.last_login = now()
        user.save()

        return Response({
            "message": "Login successful",
            "user": {
                "user_id": user.user_id,
                "email": user.email,
                "role": user.role
            }
        })