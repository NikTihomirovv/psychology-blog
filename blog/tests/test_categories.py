from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Category


class CategoryTests(APITestCase):
    """Тесты API категорий."""

    def test_category_list_is_available(self):
        Category.objects.create(name='Психология')
        Category.objects.create(name='Отношения')

        response = self.client.get('/api/categories/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data['count'], 2)