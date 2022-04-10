from django.urls import path
from . import views
from .views import RegisterView,LoginView,UserView,LogoutView,getFile
urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('upload',views.getFile,name='upload'),

]