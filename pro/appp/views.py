from cgitb import lookup
from gc import get_objects
from django.shortcuts import get_object_or_404, render
from flask import request
from itsdangerous import serializer
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import delete
from .models import Article
from .serializers import ArticleSerializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import  HttpResponse,JsonResponse, response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics
from rest_framework import mixins
from . import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import Article






#genric view set

class ArticleViewSetGenric(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = ArticleSerializers
    queryset = Article.objects.all()


#model view set
class ArticleViewSetModel(viewsets.ModelViewSet):
    serializer_class = ArticleSerializers
    queryset = Article.objects.all()





#view set

class ArticleViewSet(viewsets.ViewSet):
    lookup_field = 'pk'
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializers(articles,many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleSerializers(data=request.data)

        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request,pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset,pk=pk)
        serializer = ArticleSerializers(article)
        return Response(serializer.data)
    
    def update(self,request,pk=None):
        article = Article.objects.get(pk=pk)
        serializer = serializers.ArticleSerializers(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        article = Article.objects.get(pk=pk) 
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

























#genric api view
class GenricApiView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = ArticleSerializers
    queryset = Article.objects.all()
    lookup_field = 'id'
    # authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,id=None):
        if id:
            return self.retrieve(request)
        else:
          return self.list(request)
    def post(self,request):
         return self.create(request)
    def put(self, request,id=None):
         return self.update(request,id)
    def delete(self,request,id):
         return self.destroy(request,id)





















#class based views
class ArticleAPIView(APIView):
    def get(self,request):
        articles = Article.objects.all()
        serializer = ArticleSerializers(articles,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ArticleSerializers(data=request.data)

        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


class ArticleDetail(APIView):
    def get_object(request,id):
        try:
            return Article.objects.get(id=id)
        except:
            raise Http404
    def get(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializers(article)
        return Response(serializer.data)

    def put(self,request,id):
        article = self.get_object(id) 
        serializer = ArticleSerializers(article,data=request.data)

        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
         article = self.get_object(id) 
         article.delete()
         return Response(status = status.HTTP_204_NO_CONTENT)
























#Function based views
@api_view(['GET', 'POST'])
def article_list_by_view(request):
    if request.method == 'GET':
       a = Article.objects.all() 
       ser1 = ArticleSerializers(a,many=True)
       return Response(ser1.data)
    elif request.method == 'POST':
  
       ser2 = ArticleSerializers(data=request.data)

       if ser2.is_valid():
           ser2.save()
           return Response(ser2.data,status=status.HTTP_201_CREATED)
       return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


# single object print functio based view

@api_view(['GET', 'PUT', 'DELETE'])
def article_details(request,pk):
    try:
        a = Article.objects.get(id=pk)
    except :
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        ser1 = ArticleSerializers(a)
        return Response(ser1.data)

    elif request.method == 'PUT':
        
        ser2 = ArticleSerializers(a,data=request.data)
        if ser2.is_valid():
           ser2.save()
           return Response(ser2.data)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        a.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)






