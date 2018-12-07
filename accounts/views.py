# Create your views here.
from django.contrib import auth, messages
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import Token


def send_login_email(request):
    email = request.POST["email"]
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse("login") + "?token=" + str(token.uid))
    message_body = f"Use this link to login:\n\n{url}"
    send_mail(
        "Your login link for Superlists", message_body, "noreply@superlists", [email]
    )
    messages.success(
        request, "Check your email, we've sent you a link you can use to log in."
    )
    return redirect("/")


def login(request):
    uid = request.GET.get("token")
    user = auth.authenticate(request, uid=uid)
    if user is not None:
        auth.login(request, user)
    return redirect("/")


def logout(request):
    auth_logout(request)
    return redirect("/")
