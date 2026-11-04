from threading import Thread

from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response

from django.contrib.auth import authenticate

from django.core.exceptions import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import ProfileSerializer

from decouple import config

from cakes.utils import send_mail


# Create your views here.

class LoginView(APIView):

    def post(self,request,*args,**kwargs):

        username = request.data.get('username')

        password = request.data.get('password')

        user = authenticate(username=username,password=password)

        if user is not None:

            refresh = RefreshToken.for_user(user)

            data = {

                'refresh': str(refresh),

                'access': str(refresh.access_token),

            }

            return Response(data,status=200)

        else:

            return Response({'error':'Invalid credentials'},status=401)

   

class RegisterView(APIView):

    def post(self,request,*args,**kwargs):

        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():

            username=serializer.validated_data.get('username')

            password = serializer.validated_data.get('password')

            profile=serializer.save()

            profile.email = username

            profile.set_password(password)

            profile.save()

            receipient = profile.email

            subject = 'Welcome Abroad,Sweet Moments Await at CakeTales,'

            template = 'emails/registration.html'

            context = {'name': profile.first_name, 'email': receipient,'login_url':config('LOGIN_URL')}

            # send_mail(receipient,subject,template,context)

            thread = Thread(target=send_mail, args=(receipient, subject, template, context))

            thread.start()

            data = {'msg':'user created successfully'}

            return Response(data,status=201)

        return Response(serializer.errors,status=400)