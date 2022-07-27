from django.urls import path

from users.views import SignUpView, SignInView, MemberShipOutView

urlpatterns = [
    path("/signup", SignUpView.as_view()),
    path("/signin", SignInView.as_view()),
    path("/signquit", MemberShipOutView.as_view())
]