from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util

User = get_user_model()

class UserRegistrationSerialization(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "tc", "password", "password2"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class UserLoginSerializers(serializers.ModelSerializer):
  email = serializers.EmailField(max_length = 255)
  class Meta:
    model = User
    fields = ["email","password"]
    
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email","name"]
        
    
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255,style = {'input_type':'password'},write_only = True)
    password2 = serializers.CharField(max_length = 255,style = {'input_type':'password'},write_only = True)
    
    class Meta:
        fields = ["password","password2"]
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and confirm password doesnot match ")
        user.set_password(password)
        user.save()
        return attrs
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
        
        
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            # print('Encoded UID ',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            # print('password reset token ',token)
            link = f'http://localhost:8000/reset-password/?uid={uid}&token={token}'

            print('Password Reset Link: ',link)
            # Send Email...
            body = 'CLick Following Link to Reset your password: '+link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
                
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a registered user')
        

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255,style = {'input_type':'password'},write_only = True)
    password2 = serializers.CharField(max_length = 255,style = {'input_type':'password'},write_only = True)
    
    class Meta:
        fields = ["password","password2"]
        
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("password and confirm password doesnot match ")
            
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError('Token isnot valid or expired')
            
            user.set_password(password)
            user.save()
            return attrs    
        
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError('Token is not valid or expired! ')
        
        

