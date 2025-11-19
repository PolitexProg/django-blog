from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import DetailView
from .forms import UserCreateForm
from posts.models import Post

User = get_user_model()

class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            "form": create_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                "form": create_form
            }
            return render(request, "users/register.html", context=context)

class LoginView(View):
    def get(self,request):
        login_form = AuthenticationForm()
        return render(request,"users/login.html", {'login_form': login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home_page')
        else:
            return render(request, 'users/login.html', {'login_form': login_form})

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home_page')

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'
    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        all_posts = user.blog_posts.all()
        context['approved_posts'] = all_posts.filter(is_approved=True)
        context['pending_posts'] = all_posts.filter(is_approved=False)

        return context


