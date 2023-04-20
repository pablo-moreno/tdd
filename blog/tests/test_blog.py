import string
import random

from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class TestBlogArticles(APITestCase):
    def setUp(self) -> None:
        self.user_1 = User.objects.create(
            username='pablo',
            email='pablo@mail.com',
        )
        self.user_2 = User.objects.create(
            username='jorge',
            email='jorge@mail.com',
        )

    def test_anonymous_cannot_create_article(self):
        response = self.client.post('/api/v1/articles/', {
            'text': 'Hola mundo',
            'status': 'DRF',
            'is_private': False,
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_can_create_article(self):
        self.client.force_login(self.user_1)
        response = self.client.post('/api/v1/articles/', {
            'text': 'Hola mundo',
            'is_private': False,
        })
        assert response.status_code == status.HTTP_201_CREATED
        pk = response.data.get('id')

        # Con esto probamos que el usuario puede ver su artículo
        response = self.client.get(f'/api/v1/articles/{pk}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('text') == 'Hola mundo'
        assert response.data.get('is_private') is False

        # Por defecto, estará en estado borrador
        assert response.data.get('status') == 'DRF'

        # Comprobamos que el artículo está asociado al usuario
        assert response.data.get('user') == self.user_1.pk

    def test_user_cannot_create_article_greater_than_280_chars(self):
        self.client.force_login(self.user_1)
        response = self.client.post('/api/v1/articles/', {
            'text': ''.join(random.choices(string.ascii_uppercase + string.digits, k=300)),
            'status': 'DRF',
            'is_private': False,
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_delete_user_articles_on_user_deletion(self):
        self.client.force_login(self.user_1)

        # Creamos dos artículos para el usuario 1
        self.client.post('/api/v1/articles/', {
            'text': 'Hola mundo',
            'status': 'PUB',
            'is_private': False,
        })
        self.client.post('/api/v1/articles/', {
            'text': 'Hola mundo',
            'status': 'PUB',
            'is_private': False,
        })

        # Nos registramos como usuario 2
        self.client.force_login(self.user_2)

        # Comprobamos que hay dos artículos en total
        response = self.client.get('/api/v1/articles/')
        assert response.data.get('count') == 2

        # Borramos el usuario 1 y comprobamos que ya no hay artículos
        self.user_1.delete()
        response = self.client.get('/api/v1/articles/')
        assert response.data.get('count') == 0

    def test_articles_visibility(self):
        self.client.force_login(self.user_1)

        # Creamos dos artículos para el usuario 1
        self.client.post('/api/v1/articles/', {
            'text': 'Hola mundo',
            'status': 'PUB',
            'is_private': True,
        })
        self.client.post('/api/v1/articles/', {
            'text': 'Hola mundo',
            'status': 'PUB',
            'is_private': False,
        })
        self.client.post('/api/v1/articles/', {
            'text': 'Hola mundo',
            'status': 'DRF',
            'is_private': False,
        })
        self.client.post('/api/v1/articles/', {
            'text': 'Hola mundo',
            'status': 'DRF',
            'is_private': True,
        })

        # Nos registramos como usuario 2
        self.client.force_login(self.user_2)

        # Comprobamos que solo hay un artículo público y publicado en total
        response = self.client.get('/api/v1/articles/')
        assert response.data.get('count') == 1

    def test_article_edit(self):
        self.client.force_login(self.user_1)

        # Creamos dos artículos para el usuario 1
        response = self.client.post('/api/v1/articles/', {
            'text': 'Hola mundo',
            'status': 'DRF',
            'is_private': True,
        })

        pk = response.data.get('id')
        assert response.data.get('creation_date') == response.data.get('last_modification_date')

        response = self.client.patch(f'/api/v1/articles/{pk}/', {
            'text': 'Hola mundo 2',
            'status': 'PUB',
            'is_private': False,
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('text') == 'Hola mundo 2'
        assert response.data.get('status') == 'PUB'
        assert response.data.get('is_private') is False
        assert response.data.get('creation_date') != response.data.get('last_modification_date')

    def test_cannot_edit_other_user_article(self):
        self.client.force_login(self.user_1)

        # Creamos un artículo para el usuario 1
        response = self.client.post('/api/v1/articles/', {
            'text': 'Hola mundo',
            'status': 'PUB',
            'is_private': False,
        })

        pk = response.data.get('id')

        # Nos registramos como usuario 2 y tratamos de editarlo
        self.client.force_login(self.user_2)

        response = self.client.patch(f'/api/v1/articles/{pk}/', {
            'text': 'Hola mundo 2',
            'status': 'PUB',
            'is_private': True,
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN
