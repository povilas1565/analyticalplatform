from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import LoginForm


class LoginView(View):
    """
        Login view
    """
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        form = LoginForm(request.POST or None)
        css = "css/login.css"
        context = {'form': form, 'css': css}
        return render(request, 'account/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        form = LoginForm(request.POST or None)
        css = "css/auth.css"
        context = {'form': form, 'css': css}
        return render(request, 'account/login.html', context)
