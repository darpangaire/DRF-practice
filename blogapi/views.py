from django.shortcuts import render
from .serializers import UserRegistrationSerialization,UserLoginSerializers,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import serializers
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

# Create your views here.

def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
  
class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
      serializer = UserRegistrationSerialization(data=request.data)
      if serializer.is_valid():
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token':token,'msg':'Registration successfull'},status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class UserLoginView(APIView):
  def post(self,request,format=None):
    serializer = UserLoginSerializers(data = request.data)
    if serializer.is_valid(raise_exception=True):
      email = serializer.data.get('email')
      password = serializer.data.get('password')
      user = authenticate(email=email,password=password)
      if user:
        token = get_tokens_for_user(user)
        return Response({'msg':'Login SUCCESSFULL','token':token},status=status.HTTP_200_OK)
      
      else:
        return Response({'error':{'non_fields_errors':['Email or password isnot valid']}},status=status.HTTP_200_OK)
      
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
   
class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self,request,format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self,request,format=None):
    serializer = UserChangePasswordSerializer(data = request.data,context = {'user':request.user})
    
    if serializer.is_valid(raise_exception=True):
      return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
    
class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self,request,format=None):
    serializer = SendPasswordResetEmailSerializer(data = request.data)
    if serializer.is_valid(raise_exception = True):
      return Response({'msg':'Password Reset link send. Please check your email'},status=status.HTTP_200_OK)
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
  
class UserPasswordResetView(APIView):
  renderer_classes=[UserRenderer]
  def post(self,request,uid,token,format=None):
    serializer = UserPasswordResetSerializer(data = request.data,context ={'uid':uid,'token':token})
    
    if serializer.is_valid(raise_exception=True):
      return Response({'msg':'Password Reset Successfully'},status=status.HTTP_200_OK)
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
      
  
      
