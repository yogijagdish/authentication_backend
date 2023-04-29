from django.urls import path
from account.views import UserRegistrationView,UserLoginView,UserProfileView,UserPasswordChangeView,UserResetEmailView

urlpatterns = [
    path("createuser/",UserRegistrationView.as_view()),
    path('login/',UserLoginView.as_view()),
    path('profile/',UserProfileView.as_view()),
    path('changepassword/',UserPasswordChangeView.as_view()),
    path('sendemail/',UserResetEmailView.as_view())
]