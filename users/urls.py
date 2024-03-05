from django.urls import path
from users import views

urlpatterns = [
    path('signup/', views.signup, name='sign-up'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_view, name='logout')
]