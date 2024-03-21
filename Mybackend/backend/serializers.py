from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Images
from django.core.validators import MinLengthValidator,EmailValidator
from django.contrib.auth.password_validation import validate_password

class GetImageSerializer(serializers.ModelSerializer):
    image_uri=serializers.SerializerMethodField(method_name='get_image_uri')
    class Meta:
        model=Images
        fields=('id','name','image_uri')

    def get_image_uri(self,obj):
        return self.context['request'].build_absolute_uri(obj.image.url)
    
    

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Images
        fields=('name','image') 


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[MinLengthValidator(8, message="Password must be at least 8 characters long."),validate_password])
    class Meta:
        model=User
        fields=('username','email','password')

