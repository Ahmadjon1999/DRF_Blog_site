from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializer import UserSerializerSignup, UserSerializerSignin, UserSerializerUpdate



class SignUp(APIView):

    def get(self, request):
        return Response({
            "message": "Registratsiya saxifasi",
            "majburiy_soxalar": [
                "first_name",
                "last_name",
                "username",
                "password",
                "conf_password"
            ]
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializerSignup(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Royxatdan otish muvaffaqiyatli",
                "data":serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message":"Malumot kiritilishida xatolik",
            "data":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class SignIn(APIView):
    def get(self, request):
        return Response({
            "message":"Login saxifa",
            "majburiy soxalar":[
                "username",
                "password"
            ]
        })

    def post(self, request):
        serializer = UserSerializerSignin(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message":"Login muvaffaqqiyatli",
                "Token":token.key
            }, status=status.HTTP_200_OK)
        return Response({
                "message":"Xatolik",
            "data":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):  # ← post
        request.user.auth_token.delete()
        return Response({
            "message": "Tizimdan chiqdingiz"
        }, status=status.HTTP_200_OK)



class UpdateUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message":"Profilni o'zgartirish saxifasi",
            "O'zgartirish mumkin bolgan soxalar": [
                "first_name",
                "last_name",
                "username",
                "password"
            ]
        })

    def patch(self, request):
        user = request.user
        serializer = UserSerializerUpdate(
            user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profil yangilandi",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Xatolik",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




