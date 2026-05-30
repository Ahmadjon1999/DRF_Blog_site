from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Post, Comment, Like
from .serializers import PostSerializer

from .serializers import (SignUpSerializer,SigninSerializer,
                          Profil_detail_serializer, UserSerializerUpdate,
                          PostCreateSerializer, CommentCreateSerializer, CommentSerializer)


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
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Royxatdan otish muvaffaqiyatli",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Malumot kiritilishida xatolik",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    def get(self, request):
        return Response({
            "message": "Login saxifa",
            "majburiy soxalar": [
                "username",
                "password"
            ]
        })

    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message":"Login muvaffaqiyatli",
                "data":token.key
            }, status=status.HTTP_200_OK)
        return Response({
            "message":"Xatolik",
            "data":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = Profil_detail_serializer(user)
        return Response({
            "message": "Profil malumotlari",
            "data": serializer.data
        }, status=status.HTTP_200_OK)



class SignOut(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({
            "message":"Tizimdan chiqdingiz"
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



class PostListView(APIView):
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def get(self, request):
        posts = Post.objects.all()
        if posts:
            serializer = PostSerializer(posts, many=True)
            return Response({
                "message":"Mavjud barcha postlar",
                "data":serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message":"Xozirda postlar mavjud emas,Post qoshish uchun majburiy soxalar",
            "data":[
                'title',
                'content',
                'image',
                'category'
            ]
        }, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({
                "message":"Post saqlandi",
                "data":serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message":"Malumotlar kiritishda xatolik",
            "data":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class PostDetailView(GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return []

    def get(self, request, pk):
        post = self.get_object()
        serializer = self.get_serializer(instance=post)
        return Response({
            "message":f"id {pk} bolgan post",
            "data":serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        post = self.get_object()

        if post.author != request.user:
            return Response({
                "message":"Siz bu postni o'zgartirish xuquqiga ega emassiz"
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(instance=post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Malumotlar ozgartirildi",
                "data":serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message":"Malumotlar kiritishda xatolik",
            "data":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object()
        if post.author != request.user:
            return Response({
                "message":"Siz bu postni o'chirish xuquqiga ega emassiz"
            }, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({
            "message":"Post o'chirildi"
        }, status=status.HTTP_204_NO_CONTENT)



class SearchPosts(APIView):
    def get(self, request):
        posts = Post.objects.all()

        search = request.query_params.get('search', None)
        if search:
            posts = posts.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(category__name__icontains=search)
            )

        category = request.query_params.get('category', None)
        if category:
            posts = posts.filter(category__name__icontains=category)

        ordering = request.query_params.get('ordering', None)
        if ordering:
            posts = posts.order_by(ordering)

        serializer = PostSerializer(instance=posts, many=True)
        return Response({
            "message": "Qidiruv natijasi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)



class CommentListView(GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return []

    def get(self, request):
        comments = self.get_queryset()
        if comments.exists():
            serializer = CommentSerializer(instance=comments, many=True)
            return Response({
                "message": "Mavjud barcha izoxlar",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message":"Xozirda Izoxlar mavjue emas"
        }, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"message": f"{pk} id li post mavjud emas"}, status=404)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response({
                "message":"Izox saqlandi",
                "data":serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message":"Malumot kiritishda xatolik"
        }, status=status.HTTP_400_BAD_REQUEST)



class CommentDetailView(GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return []

    def get(self, request, pk):
        comment = self.get_object()
        serializer = CommentSerializer(instance=comment)
        return Response({
            "message": f"{pk} i siga teng izox",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        comment = self.get_object()
        if comment.user != request.user:
            return Response({
                "message": "Sizda ruxsat yo'q"
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentCreateSerializer(instance=comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Izox yangilandi",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Malumotlar kiritishda xatolik",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object()
        if comment.user != request.user:
            return Response({
                "message": "Sizda ruxsat yo'q"
            }, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({
            "message":"Izox o'chirildi"
        }, status=status.HTTP_204_NO_CONTENT)



class LikeView(APIView):
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return []

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"message": f"{pk} id li post mavjud emas"}, status=404)

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            return Response(
                {
                    "message": "Like bosildi"
                 }, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({
                "message": "Like olib tashlandi"
            }, status=status.HTTP_200_OK)















