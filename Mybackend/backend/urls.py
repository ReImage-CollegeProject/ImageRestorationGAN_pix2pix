from django.urls import path
from .views import hanlde_image,register_view,login_view,get_Image,logout_view,cvt_img,delete_image


urlpatterns=[
    path('api/register',register_view,name="register"),
    path('api/login',login_view,name="login"),
    path('api/logout',logout_view,name="logout"),
    path('api/upload',hanlde_image,name="upload"),
    path('api/convert_image/<int:pk>',cvt_img,name="convert"),
    path('api/delete_image/<int:pk>',delete_image,name="delete"),
    path('api/get',get_Image),
]