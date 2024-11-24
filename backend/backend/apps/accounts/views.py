from django.contrib import messages
from django.contrib.auth import (login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ChangePasswordForm, EditProfileForm, SignInForm, SignUpForm


def home(request):
    return render(request, 'authenticate/home.html')


def login_user(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Сіз жүйеге сәтті кірдіңіз!')
            return redirect('pages:home')
        else:
            messages.error(request, 'Қате пайдаланушы аты немесе құпия сөз!')
    else:
        form = SignInForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('pages:home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 'Тіркелу сәтті аяқталды! Енді жүйеге кіріңіз.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Тіркеуде қателіктер бар!')
    else:
        form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Профиль жаңартылды!')
            return redirect('accounts:edit_profile')
        else:
            messages.error(request, 'Жаңартуда қателіктер бар!')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {
        'form': form,
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Құпия сөз сәтті жаңартылды!')
            return redirect('accounts:edit_profile')
        else:
            messages.error(request, 'Құпия сөзді жаңартуда қателіктер бар!')
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'accounts/change_password.html', {'form': form})
