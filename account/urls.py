from django.urls import path
from account.views import UserRegistrationView

urlpatterns = [
    path("createuser/",UserRegistrationView.as_view())
]