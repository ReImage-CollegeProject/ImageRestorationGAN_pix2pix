from django.test import TestCase
from django.contrib.auth.models import User
from backend.models import  Images, ConvertedImg

class ImagesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='testpassword')

        Images.objects.create(user=test_user, name='Test Image', image='images/test_image.jpg')

    def test_user_label(self):
        image = Images.objects.get(id=1)
        field_label = image._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')
        print("usertest .. ok")

    def test_name_label(self):
        image = Images.objects.get(id=1)
        field_label = image._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
        print("image name test ...ok")

    def test_image_label(self):
        image = Images.objects.get(id=1)
        field_label = image._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'image')
        print("Image label test .. ok")

    def test_name_max_length(self):
        image = Images.objects.get(id=1)
        max_length = image._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)
        print("image name lenght test ... ok")


class ConvertedImgModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='testpassword')

        image = Images.objects.create(user=test_user, name='Test Image', image='images/test_image.jpg')

        ConvertedImg.objects.create(name=image, img='converted_image/test_converted_image.jpg')

    def test_name_label(self):
        converted_image = ConvertedImg.objects.get(id=1)
        field_label = converted_image._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

        print("ConvertImage name test .. ok")

    def test_img_label(self):
        converted_image = ConvertedImg.objects.get(id=1)
        field_label = converted_image._meta.get_field('img').verbose_name
        self.assertEqual(field_label, 'img')
        print("Image label test .. ok")

