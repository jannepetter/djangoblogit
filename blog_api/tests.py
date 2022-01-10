from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from blog.models import Post, Category
from django.contrib.auth.models import User
from users.models import NewUser


class PostTests(APITestCase):
    def test_view_posts(self):
        """
        Ensure we can view all objects.
        """
        url = reverse("blog_api:post-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        """
        Ensure we can create a new Post object and view object.
        """
        self.test_category = Category.objects.create(name="django")
        self.testuser1 = NewUser.objects.create_user(
            user_name="test_user1",
            first_name="firstName",
            password="123456789",
            email="test@testitest.com",
        )
        # self.testuser1.is_staff = True
        tokenurl = reverse("token_obtain_pair")
        logindata = {"email": "test@testitest.com", "password": "123456789"}
        tokens = self.client.post(tokenurl, logindata, format="json")
        accessToken = tokens.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION="JWT " + accessToken)
        data = {"title": "new", "excerpt": "new", "content": "new"}
        url = reverse("blog_api:post-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_post_update(self):

    #     client = APIClient()

    #     self.test_category = Category.objects.create(name="django")
    #     self.testuser1 = User.objects.create_user(
    #         username="test_user1", password="123456789"
    #     )
    #     self.testuser2 = User.objects.create_user(
    #         username="test_user2", password="123456789"
    #     )
    #     test_post = Post.objects.create(
    #         category_id=1,
    #         title="Post Title",
    #         excerpt="Post Excerpt",
    #         content="Post Content",
    #         slug="post-title",
    #         author_id=1,
    #         status="published",
    #     )

    #     client.login(username=self.testuser1.username, password="123456789")

    #     url = reverse(("blog_api:detailcreate"), kwargs={"pk": 1})

    #     response = client.put(
    #         url,
    #         {
    #             "title": "New",
    #             "author": 1,
    #             "excerpt": "New",
    #             "content": "New",
    #             "status": "published",
    #         },
    #         format="json",
    #     )
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
