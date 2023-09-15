from django.urls import path
from users import views


urlpatterns = [
    path('', views.NetworkUsersList.as_view()),
    path('<int:pk>/', views.NetworkUserInfo.as_view()),

    # not sure about this in users app
    path('signup/', views.CreateNetworkUser.as_view()),
]

