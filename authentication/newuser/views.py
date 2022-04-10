from time import sleep

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import io
import pandas as pd
import string
import random
import os
import bcrypt
import requests

from location import location
from .helpers import parseExcel
from .serializers import newuserserializer
from .models import newusers
import jwt, datetime


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        print("request data", request.data)
        password = request.data['password']
        # Encode the stored password:
        password = password.encode('utf-8')
        # Encrypt the stored password:
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(10))
        print('hashed', hashed_password.decode('utf-8'))
        request.data['password'] = hashed_password.decode('utf-8')
        serializer = newuserserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        password = password.encode('utf-8')
        print('password', password)
        user = newusers.objects.filter(email=email).first()
        expected_password = user.password.encode('utf-8')
        print('expected pwd', expected_password)
        if user is None:
            raise AuthenticationFailed('User Not found')
        if not bcrypt.checkpw(password, expected_password):
            raise AuthenticationFailed('Incorrect Password')
        # if user.password != password:
        #     raise AuthenticationFailed('Incorrect Password')
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', 'HS256').decode('utf-8')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True, secure=True)
        response.cookies['jwt'].update({"samesite": "None"})
        print('cookie', response.cookies['jwt'])
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed('Unauthenticated user')
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            print(payload)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('token expired')
        user = newusers.objects.filter(id=payload['id']).first()
        print('user',user)
        serializer = newuserserializer(user)
        print('serializer',serializer.data)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        #print("hi",response.cookies)
        #response.delete_cookie('jwt')
        token=""
        response.set_cookie(key='jwt', value=token, httponly=True, secure=True)
        print(response.cookies)
        response.data = {
            'message': 'success!'
        }
        return response


@api_view(['POST'])
def getFile(request):
    data = request.data['file']
    data = io.StringIO(data)
    df = pd.read_csv(data, sep=",")

    print("data", df)
    letters = string.ascii_lowercase

    # determining the name of the file
    file_name = ''.join(random.choice(letters) for i in range(10))
    file_name += '.xlsx'
    # saving the excel

    df.to_excel(file_name,index=False)
    print('filename', file_name)
    #parseExcel(file_name)
    location()
    os.remove(file_name)
    return Response()
