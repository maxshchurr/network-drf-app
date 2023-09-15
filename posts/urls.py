from django.urls import path
from posts import views


urlpatterns = [
        path('', views.PostList.as_view()),
        path('<int:pk>/', views.PostInfo.as_view()),
        path('create-post/', views.CreatePost.as_view()),
]
