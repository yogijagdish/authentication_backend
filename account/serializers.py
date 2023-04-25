## importing files provided by rest framework
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

## importing files that exists within this folders
from account.models import User
from account.utils import Util


## for encoding and sending the reset link to the email
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


## serializers to handle registration of new user and allowing validation and creating of new user
class UserRegistrationSerializer(ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ["email","name","password","password2"]
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password Doesnot Match')
        return attrs

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


## serializers for handling login of existing user
class UserLoginSerializer(ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ["email","password"]

class UserProfileSerializer(ModelSerializer): 
    class Meta:
        model = User
        fields = ["id","email","name"]

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password doesnot match")

        user.set_password(password)
        user.save()
        return attrs

class UserResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator.make_token(user)
            link = "http://127.0.0.1:3000/"+uid+"/"+token
            data = {
                'subject':'Reset your Email',
                'body':'Click the following link to chhnage your password',
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs

        else:
            raise serializers.ValidationError('you are not registered user')


class UserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesnot match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError("Token is invalid or expired")
            
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError("Token is expired or invalid")
