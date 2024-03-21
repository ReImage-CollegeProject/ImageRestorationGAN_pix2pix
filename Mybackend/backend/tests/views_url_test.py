from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from backend.models import Images

from django.core.files.uploadedfile import SimpleUploadedFile
class Backedns(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.image_path = '/Users/nihang/Desktop/ReImage/Mybackend/backend/imagetestcase/image-1200x1200.png'
        with open(self.image_path, 'rb') as f:
            self.image = SimpleUploadedFile("test_image.png", f.read(), content_type="image/png")

    def test_register(self):
        url = reverse('register')  
        data = {'username': 'nihang','email':'test@gmail.com' ,'password': 'nihang#123'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_login(self):
        url = reverse('login')  
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_logout(self):
        url = reverse('logout')  
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'User logged out')

    def test_handle_image(self):
        url = reverse('upload')  
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        data = {'name':'hellotest','image': self.image}
        response = self.client.post(url, data, format='multipart')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image', response.data)
        

    def test_convert_image(self):
        image_instance = Images.objects.create(user=self.user, name="hellotest",image=self.image)

        url = reverse('convert', kwargs={'pk': image_instance.id})  
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        data = {'type': 'dilate', 'size': 15}  
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image', response.data)
