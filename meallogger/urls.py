from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from meallogger.forms import CustomAuthForm


urlpatterns = [
    path('accounts/login/', auth_views.login,
         {'template_name': 'accounts/login.html',
          'authentication_form': CustomAuthForm}, name='login'),
    path('accounts/logout/', auth_views.logout,
         {'next_page': '/accounts/login/'}, name='logout'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),

    path('<str:username>/', views.UserMeals.as_view(), name='usermeals'),
    path('', views.HomeView.as_view(), name='home'),
]
