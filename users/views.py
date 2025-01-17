from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from data.models import Accident, Message
from data.forms import AccidentForm
from .models import CustomUser

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
    unread_messages = Message.objects.filter(user=user, read=False)
    return render(request, 'users/user_dashboard.html', {'accidents': accidents, 'unread_messages': unread_messages})

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

@login_required
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    previous_url = request.META.get('HTTP_REFERER', 'default_url')
    return render(request, 'users/user_detail.html', {'user': user, 'previous_url': previous_url})