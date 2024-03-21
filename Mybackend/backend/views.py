import os
from rest_framework.response import Response
from .serializers import ImageSerializer,UserSerializer,GetImageSerializer
from rest_framework.decorators import api_view,parser_classes,permission_classes,authentication_classes
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser
from rest_framework import status
from .models import ConvertedImg,Images
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import pathlib
import torch
from torchvision import transforms
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
import cv2 as cv

import torch
from torch import nn
import torch.nn.functional as F

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_Image(request):
    obj=Images.objects.filter(user=request.user)
    serializer=GetImageSerializer(obj,context={"request":request} ,many=True)
    if serializer.data:
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response("user has not uploaded any images",status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def register_view(request):
    if request.method=='POST':
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user=User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token=Token.objects.create(user=user)
            return Response({"token":token.key,'user':serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
            
@api_view(['POST'])
def login_view(request):
    user=get_object_or_404(User,username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"error":"User not found"},status=status.HTTP_404_NOT_FOUND)
    token,create=Token.objects.get_or_create(user=user)
    serializer=UserSerializer(user)
    return Response({'token':token.key,"user":serializer.data},status=status.HTTP_200_OK)
      

@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.auth.delete()
    return Response("User logged out",status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_image(request,pk):
    obj=get_object_or_404(Images,id=pk)
    obj.delete()
    return Response({"message":"image deleted"},status=status.HTTP_200_OK)



@api_view(['POST'])
@parser_classes([MultiPartParser,FormParser])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])

def hanlde_image(request):
    if request.method=="POST":
        serializer=ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            imgobj=serializer.instance
            id=imgobj.id
            print("id: "+str(id))
            return Response({"id":id},status=status.HTTP_200_OK)
        else:
            serializer=ImageSerializer()
            return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])

def cvt_img(request,pk):
    obj=get_object_or_404(Images,id=pk)
    image_path=os.getcwd()+obj.image.url
    xml_path=("/Users/nihang/Desktop/ReImage/Mybackend/backend/Autoencoder/haarcascade_frontalface_default.xml")
    face_classifier=cv.CascadeClassifier(xml_path)
    image=cv.imread(image_path)
    grey_img=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    face=face_classifier.detectMultiScale(grey_img,scaleFactor=1.1,minNeighbors=5)

    # if type(face)!=tuple:
    extn=pathlib.Path(image_path).suffix
    try:
        got_image = ConvertedImg.objects.filter(name__name=obj.name)
        got_image.delete()
    except AttributeError:
        print("not found")


    image=Image.open(image_path).convert("RGB")
    processed_image = preprocess_image(image)
    GAN_model = UnetGenerator()
    state_dict = torch.load("/Users/nihang/Desktop/ReImage/Mybackend/backend/Autoencoder/generator_epoch_70.pth", map_location=torch.device("cpu"))


    if next(iter(state_dict.keys())).startswith("module"):
        state_dict = {key[7:]: value for key, value in state_dict.items()}

    GAN_model.load_state_dict(state_dict)
    GAN_model.eval()

    with torch.no_grad():
        denoised_image = GAN_model(processed_image)

    postprocessed_image = postprocess_image(denoised_image)
    model_instance = ConvertedImg()

    image_bytes = BytesIO()
    postprocessed_image.save(image_bytes, format='JPEG')
    model_instance.name=obj
    model_instance.img.save(obj.name + '_denoised' + extn, ContentFile(image_bytes.getvalue()))
    model_instance.save()

    img_url = ConvertedImg.objects.get(name__name=obj.name)
    return Response({"image":request.build_absolute_uri(img_url.img.url)},status=status.HTTP_200_OK)
    # else:
    #     return Response({"error_messages":"face not found in image"},status=status.HTTP_400_BAD_REQUEST)


def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        
    ])
    processed_image = transform(image).unsqueeze(0)
    return processed_image


def postprocess_image(denoised_image_tuple):

    denoised_image=denoised_image_tuple[0]
    STATS = (0.5, 0.5, 0.5), (0.5, 0.5, 0.5)
    myimage=denoised_image * STATS[1][0] + STATS[0][0]
    postprocessed_image = transforms.ToPILImage()(myimage.squeeze(0))
    return postprocessed_image




class UnetGenerator(nn.Module):
    """Unet-like Encoder-Decoder model"""

    def __init__(
        self,
    ):
        super().__init__()

        self.encoder1 = nn.Conv2d(3, 64, kernel_size=4, stride=2, padding=1)
        self.encoder2 = EncoderBlock(64, 128)
        self.encoder3 = EncoderBlock(128, 256)
        self.encoder4 = EncoderBlock(256, 512)
        self.encoder5 = EncoderBlock(512, 512)
        self.encoder6 = EncoderBlock(512, 512)
        self.encoder7 = EncoderBlock(512, 512)
        self.encoder8 = EncoderBlock(512, 512, norm=False)

        self.decoder8 = DecoderBlock(512, 512, dropout=True)
        self.decoder7 = DecoderBlock(2 * 512, 512, dropout=True)
        self.decoder6 = DecoderBlock(2 * 512, 512, dropout=True)
        self.decoder5 = DecoderBlock(2 * 512, 512)
        self.decoder4 = DecoderBlock(2 * 512, 256)
        self.decoder3 = DecoderBlock(2 * 256, 128)
        self.decoder2 = DecoderBlock(2 * 128, 64)
        self.decoder1 = nn.ConvTranspose2d(
            2 * 64, 3, kernel_size=4, stride=2, padding=1
        )

    def forward(self, x):
        # encoder forward
        e1 = self.encoder1(x)
        e2 = self.encoder2(e1)
        e3 = self.encoder3(e2)
        e4 = self.encoder4(e3)
        e5 = self.encoder5(e4)
        e6 = self.encoder6(e5)
        e7 = self.encoder7(e6)
        e8 = self.encoder8(e7)
        # decoder forward + skip connections
        d8 = self.decoder8(e8)
        d8 = torch.cat([d8, e7], dim=1)
        d7 = self.decoder7(d8)
        d7 = torch.cat([d7, e6], dim=1)
        d6 = self.decoder6(d7)
        d6 = torch.cat([d6, e5], dim=1)
        d5 = self.decoder5(d6)
        d5 = torch.cat([d5, e4], dim=1)
        d4 = self.decoder4(d5)
        d4 = torch.cat([d4, e3], dim=1)
        d3 = self.decoder3(d4)
        d3 = torch.cat([d3, e2], dim=1)
        d2 = F.relu(self.decoder2(d3))
        d2 = torch.cat([d2, e1], dim=1)
        d1 = self.decoder1(d2)

        return torch.tanh(d1)
    
class EncoderBlock(nn.Module):
    """Encoder block"""

    def __init__(
        self, inplanes, outplanes, kernel_size=4, stride=2, padding=1, norm=True
    ):
        super().__init__()
        self.lrelu = nn.LeakyReLU(0.2, inplace=True)
        self.conv = nn.Conv2d(inplanes, outplanes, kernel_size, stride, padding)

        self.bn = None
        if norm:
            self.bn = nn.BatchNorm2d(outplanes)

    def forward(self, x):
        fx = self.lrelu(x)
        fx = self.conv(fx)

        if self.bn is not None:
            fx = self.bn(fx)

        return fx


class DecoderBlock(nn.Module):
    """Decoder block"""

    def __init__(
        self, inplanes, outplanes, kernel_size=4, stride=2, padding=1, dropout=False
    ):
        super().__init__()
        self.relu = nn.ReLU(inplace=True)
        self.deconv = nn.ConvTranspose2d(
            inplanes, outplanes, kernel_size, stride, padding
        )
        self.bn = nn.BatchNorm2d(outplanes)

        self.dropout = None
        if dropout:
            self.dropout = nn.Dropout2d(p=0.5, inplace=True)

    def forward(self, x):
        fx = self.relu(x)
        fx = self.deconv(fx)
        fx = self.bn(fx)

        if self.dropout is not None:
            fx = self.dropout(fx)

        return fx
