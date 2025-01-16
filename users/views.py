from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from data.models import Accident 
from data.forms import AccidentForm


def is_admin(user):
    return user.is_staff

def register(request):
    if request.method == 'POST':
        form =CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            phone = form.cleaned_data.get('phone_number')
            address = form.cleaned_data.get('address')
            messages.success(request, f'Account created for {username}!')
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

def redirect_after_login(request):
    if request.user.is_admin:
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')
    
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        messages.error(request, "您没有访问管理员仪表盘的权限。")
        return redirect('user_dashboard')
    accidents = Accident.objects.filter(is_deleted=False)
    return render(request, 'users/admin_dashboard.html', {'accidents': accidents})

@login_required
def user_dashboard(request):
    user = request.user
    if user.is_staff:
        accidents = Accident.objects.filter(is_deleted=False)
    else:
        # 否则显示当前用户提交的事故记录
        accidents = Accident.objects.filter(created_by=user)

    return render(request, 'users/user_dashboard.html', {'accidents': accidents})

def is_superadmin(user):
    return user.is_superuser

@user_passes_test(is_superadmin)
def register_admin(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Admin account created for {username}!')
            return redirect("admin_dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register_admin.html', {'form': form})