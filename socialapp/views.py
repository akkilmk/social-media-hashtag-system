from operator import pos
from django.shortcuts import render
from requests import delete
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, PostManagerSerializer,SerachSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from .models import PostManager
from django.db.models.aggregates import Count
# Create your views here.


class SignUp(APIView):
    def get(self, req):
        queryset = User.objects.all()
        serializer = RegistrationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            request.session['username'] = username
            return Response(status=status.HTTP_200_OK)

    def get(self, request):
        if 'username' in request.session:
            del request.session['username']
            return Response(status=status.HTTP_200_OK)
        else:
            print('okkk')
            return Response(status=status.HTTP_202_ACCEPTED)


class CreatePost(APIView):
    def post(self, request):
        if 'username' in request.session:
            post_details = PostManagerSerializer(data=request.data)
            if post_details.is_valid():
                post_details.save()
                return Response(status=status.HTTP_200_OK)
            return Response(post_details.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if 'username' in request.session:
            post_details = PostManager.objects.only('hashtag')
            list =[]
            for i in post_details:
                if i.hashtag not in list: 
                    list.append(i.hashtag)
            return Response(list)

    def put(self,request):
        if 'username' in request.session:
            id = request.data['id']
            item = PostManager.objects.get(id = id)
            item.hashtag = request.data['hashtag']
            item.image = request.data['image']
            item.save()
            return Response(status=status.HTTP_200_OK)
    
    def delete(self,request):
        if 'username' in request.session:
            id = request.data['id']
            user_id = request.data['user_id']
        try:
            PostManager.objects.filter(id=id, user_id=user_id).delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class Trending(APIView):
    
    def get(self,request):
        if 'username' in request.session:
            post_details = PostManager.objects.values('hashtag').annotate(posts =
            Count('hashtag')).order_by('-posts')
            return Response(post_details)
    
class SerachHashtag(APIView):

    def get(self,request,format = None):
        if 'username' in request.session:
            value = request.data['hashtag']
            post_details = PostManager.objects.filter(hashtag=value)
            serializer = SerachSerializer(post_details,many =True)
            return Response(serializer.data)

