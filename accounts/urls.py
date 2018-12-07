from django.urls import path, re_path

from accounts import views

urlpatterns = [
    path("send_login_email/", views.send_login_email, name="send_login_email"),
    re_path(r"^login$", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]
