from django.shortcuts import render
from .serializers import UserRegistrationSerialization,UserLoginSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth import authenticate

# Create your views here.
class UserRegistrationView(APIView):

  def post(self,request,format=None):
    serializer = UserRegistrationSerialization(data = request.data)
    if serializer.is_valid(raise_exception=True):
      user = serializer.save()
      return Response({'msg':'Registration successfull'},status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
  
class UserLoginView(APIView):
  def post(self,request,format=None):
    serializer = UserLoginSerializers(data = request.data)
    if serializer.is_valid(raise_exception=True):
      email = serializer.data.get('email')
      password = serializer.data.get('password')
      user = authenticate(email=email,password=password)
      if user:
        return Response({'msg':'Login SUCCESSFULL'},status=status.HTTP_200_OK)
      
      else:
        return Response({'error':{'non_fields_errors':['Email or password isnot valid']}},status=status.HTTP_200_OK)
      
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  
   
  
  
  

    
