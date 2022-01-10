from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PostList, PostListausta

app_name = "blog_api"

router = DefaultRouter()

router.register("", PostList, basename="post")
urlpatterns = [
    path("posts/<str:pk>/", PostListausta.as_view(), name="detailcreate"),
]
urlpatterns += router.urls

# urlpatterns = [
#     path("<int:pk>/", PostDetail.as_view(), name="detailcreate"),
#     path("", PostList.as_view(), name="listcreate"),
# ]
