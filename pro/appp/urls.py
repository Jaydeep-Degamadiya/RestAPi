
from django import urls
from django.urls import path,include
from appp import views
from .views import ArticleAPIView,ArticleDetail,GenricApiView,ArticleViewSet,ArticleViewSetGenric,ArticleViewSetModel
from rest_framework.routers import DefaultRouter

#create and register router
router = DefaultRouter()
router.register('articleView',views.ArticleViewSet,basename='article')
router.register('articleViewgenric',views.ArticleViewSetGenric,basename='articelGen')
router.register('articleViewModel',views.ArticleViewSetModel,basename='articleModel')



urlpatterns = [
    
    
    path('article/<int:pk>',views.article_details),
    path('articleClass',ArticleAPIView.as_view()),
    path('articleview',views.article_list_by_view),
    path('articleClass/<int:id>',ArticleDetail.as_view()),
    path('articleGenric/<int:id>',GenricApiView.as_view()),
    path('articleVS/',include(router.urls)),
    path('articleVSG/',include(router.urls)),
    path('articleVSM/',include(router.urls)),


]
