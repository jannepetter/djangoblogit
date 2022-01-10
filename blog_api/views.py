from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from blog.models import Post
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissionsOrAnonReadOnly,
    DjangoModelPermissions,
    BasePermission,
)


class PostUserWritePermission(BasePermission):
    message = "Editing is restricted to author only"

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return True
        return request.user == obj.author


class PostList(viewsets.ModelViewSet):
    permission_classes = [PostUserWritePermission]
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.postobjects.all()

    # def get_permissions(self):
    #     if self.action == "list":
    #         permission_classes = [IsAuthenticated]
    #         return [permission() for permission in permission_classes]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")
        return get_object_or_404(Post, id=item)

    def create(self, request, *args, **kwargs):
        print("postausta------------------", request.user, request.data)
        postaus = {
            **request.data,
            "slug": request.data["title"].replace(" ", "-").replace("ä", "a"),
            "author": request.user.pk,
        }
        serializer = self.get_serializer(data=postaus)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        print("request", request.data["title"])
        sluggersson = request.data["title"].replace(" ", "-").replace("ä", "a")
        print("sluggersson", sluggersson)
        postaus = {
            **request.data,
            "slug": sluggersson,
            "author": request.user.pk,
        }
        serializer = self.get_serializer(instance, data=postaus, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class PostListausta(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = (
        Post.postobjects.all()
    )  # mallissa luotiin postobjects joka palauttaa published
    serializer_class = PostSerializer

    def get_queryset(self):
        item = self.kwargs["pk"]
        print("itemia postlistauksessa", item)
        return Post.postobjects.filter(title=item)


# class PostList(viewsets.ViewSet):
#     permission_classes = [AllowAny]
#     queryset = Post.postobjects.all()

#     def list(self, request):
#         serializer_class = PostSerializer(self.queryset, many=True)
#         return Response(serializer_class.data)

#     def retrieve(self, request, pk=None):
#         post = generics.get_object_or_404(self.queryset, pk=pk)
#         serializer_class = PostSerializer(post)
#         return Response(serializer_class.data)


# class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
#     permission_classes = [PostUserWritePermission]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     pass
