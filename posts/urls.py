from django.urls import path
from posts import views


urlpatterns = [
        path('', views.PostList.as_view()),
        path('<int:pk>/', views.PostInfo.as_view()),
        path('<int:pk>/like/', views.PostLike.as_view()),
        path('create-post/', views.CreatePost.as_view()),

        path('api/analitics/', views.LikesAnalyticsView.as_view(), name='likes-analytics'),

]
