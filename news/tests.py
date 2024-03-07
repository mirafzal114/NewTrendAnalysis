from django.test import TestCase
from django.contrib.auth.models import User
from .models import News

class NewsViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.post = News.objects.create(
            title='Test News',
            body='This is a test news post.',
            author=self.user,
            status=News.Status.PUBLISHED
        )

    def test_news_list_view(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/home.html')

    def test_news_detail_view(self):
        response = self.client.get(f'/news/{self.post.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_detail.html')
        self.assertContains(response, 'Test News')

    def test_post_share_view(self):
        response = self.client.get(f'/news/{self.post.id}/share/')
        self.assertEqual(response.status_code, 302)

    def test_post_comment_view(self):
        response = self.client.get(f'/news/{self.post.id}/comment/')
        self.assertEqual(response.status_code, 302)

    def test_create_news_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/news/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/addnews.html')

    def test_delete_news_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(f'/news/{self.post.id}/delete/')
        self.assertEqual(response.status_code, 302)

    def test_search_product_view(self):
        response = self.client.get('/search/', {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'Test News')
