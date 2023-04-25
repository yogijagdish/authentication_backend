## importing files given by django
from django.contrib.auth import authenticate

## importing files from rest framwork
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

## importing files from application within this folders
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserResetEmailSerializer, UserChangePasswordSerializer,UserResetPasswordSerializer
from account.renderer import ErrorRenderes

## importing library from simple jwt for token authentication
from rest_framework_simplejwt.tokens import RefreshToken


## function that will create token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

## class to handle registration of new user
class UserRegistrationView(APIView):
    renderer_classes = [ErrorRenderes]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            ## it will generate token if the user is registered correctly and returns that token as a response to frontend
            token = get_tokens_for_user(user)
            return Response({'token':token,"msg":"User Registration Sucessful"},status=status.HTTP_201_CREATED)
        return Response({"msg":"User Registration Unsucessful"},status=status.HTTP_400_BAD_REQUEST)

## class to handle log in of existing user
class UserLoginView(APIView):
    renderer_classes = [ErrorRenderes]
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:

                ## it will generate token if the user has loged in with correct email and password and send this token with response to frontend
                token = get_tokens_for_user(user)
                return Response({'token':token,"msg":"Log in sucessful"},status=status.HTTP_200_OK)
            else:
                return Response({"errors":{"non_field_errors":['email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

## class to handle to view after authorization
class UserProfileView(APIView):
    renderer_classes = [ErrorRenderes]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)


## class to handle when user tries to change its password
class UserPasswordChangeView(APIView):
    renderer_classes = [ErrorRenderes]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password Sucessfully Changed"},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


## class to handle when user tries to access its email link to reset its password
class UserResetEmailView(APIView):
    renderer_classes = [ErrorRenderes]
    def post(self,request,format=None):
        serializer = UserResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"sending the email reset link in your email id"},status=status.HTTP_200_OK)
        else:
            return Response({"msg":"email reset failed"},status=status.HTTP_400_BAD_REQUEST)

## class to handle when user tries to reset its email
class UserResetPasswordView(APIView):
    renderer_classes = [ErrorRenderes]
    def post(self,request,uid,token,format=None):
        serializer = UserResetPasswordSerializer(data = request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Passowrd Reset Sucessful"},status=status.HTTP_200_OK)

        return Response({"msg":"User Password Unsucessful"},status=status.HTTP_400_BAD_REQUEST)



            
