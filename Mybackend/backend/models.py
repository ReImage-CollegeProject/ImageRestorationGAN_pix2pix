from django.db import models
from django.contrib.auth.models import User


class Images(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to='images/')

    def __str__(self) -> str:
        return self.name

class ConvertedImg(models.Model):
    name=models.OneToOneField(Images,on_delete=models.CASCADE,unique=True)
    img=models.ImageField(upload_to='converted_image/')

    def __str__(self) -> str:
        return self.name.name
