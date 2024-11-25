from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
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
            messages.success(request, 'Вы успешно вошли в систему!')
            next_url = request.GET.get('next') or request.POST.get('next')
            next_url = next_url or "pages:home"
            print("next_url", next_url)
            return redirect(next_url)
        else:
            messages.error(request, 'Неверное имя пользователя или пароль!')
    else:
        form = SignInForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('pages:home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 'Регистрация успешно завершена! Теперь войдите в систему.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Есть ошибки в регистрации!')
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
            messages.success(request, 'Профиль обновлен!')
            return redirect('accounts:edit_profile')
        else:
            messages.error(request, 'Есть ошибки при обновлении!')
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
            messages.success(request, 'Пароль успешно обновлен!')
            return redirect('accounts:edit_profile')
        else:
            messages.error(request, 'Есть ошибки при обновлении пароля!')
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'accounts/change_password.html', {'form': form})
