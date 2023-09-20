from django.urls import path
from  . import views

urlpatterns = [
    #login and register
    path('login/', views.loginPage , name="login"),
    path('logout/', views.logoutUser , name="logout"),
    path('register/', views.registerPage , name="register"),
    # Home and Room
    path('',  views.home, name="home"),
    path('room/<str:pk>', views.room, name="room"),
    # create, updade and delete Room;
    path('create-room/', views.createRoom , name="create-room"),
    path('update-room/<str:pk>', views.updateRoom , name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom , name="delete-room"),
    #Delete Message
    path('delete-message/<str:pk>', views.deleteMessage , name="delete-message"),
    #User Profile
    path('user-profile/<str:pk>', views.userProfilePage , name="user-profile")

]