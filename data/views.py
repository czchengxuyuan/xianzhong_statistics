from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccidentForm
from .models import Accident, Message
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib import messages

# Create your views here.

@login_required
def create_accident(request):
    if request.method == 'POST':
        form = AccidentForm(request.POST)
        if form.is_valid():
            accident = form.save(commit=False)
            accident.created_by = request.user
            accident.is_approved = False
            accident.save()
            messages.success(request, '事故记录已成功提交！')
            return redirect('accident_list')
    else:
        form = AccidentForm()
    return render(request, 'data/create_accident.html', {'form': form})

@login_required
def accident_edit(request, accident_id):
    user = request.user
    accident = get_object_or_404(Accident, id=accident_id)

    if accident.created_by != user and not user.is_staff:
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = AccidentForm(request.POST, instance=accident)
        if form.is_valid():
            form.save()
            messages.success(request, '事故记录已成功更新！')
            return redirect('user_dashboard')
    else:
        form = AccidentForm(instance=accident)
    return render(request, 'data/accident_edit.html', {'form': form})

@login_required
def accident_delete_user(request, accident_id):
    user = request.user
    accident = get_object_or_404(Accident, id=accident_id)
    if accident.created_by != user:
        return redirect('user_dashboard')
    else:
        accident.delete()
        messages.success(request, '事故记录已成功删除！')
    return redirect('user_dashboard')

@login_required
def mark_message_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.is_read = True
    message.save()
    return redirect('user_dashboard')

@login_required
def accident_list(request):
    if request.user.is_staff:
        accidents = Accident.objects.all()
    else:
        accidents = Accident.objects.filter(Q(created_by=request.user) & Q(is_approved=True) | Q(is_approved=False))
    return render(request, 'data/accident_list.html', {'accidents': accidents})

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_review_accident(request):
    accidents_to_review = Accident.objects.filter(is_approved=False)
    print(accidents_to_review)
    return render(request, 'data/admin_review_accidents.html', {'accidents': accidents_to_review})

@user_passes_test(is_admin)
def approve_accident(request, accident_id):
    accident = get_object_or_404(Accident, id=accident_id)
    if not accident.is_approved:
        accident.is_approved = True
        accident.save()

        messages.success(request, 'Accident {accident.address} approved successfully.')
        user = accident.created_by
        Message.objects.create(user=user, content=f"您的事故记录' {accident.address}' 已审核通过")

    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def reject_accident(request, accident_id):
    accident = get_object_or_404(Accident, id=accident_id)
    if not accident.is_approved:
        accident.is_approved = False
        accident.save()

        messages.success(request, 'Accident {accident.address} rejected successfully.')
        user = accident.created_by
        Message.objects.create(user=user, content=f"您的事故记录' 已被拒绝")

    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def delete_accident(request, accident_id):
    accident = get_object_or_404(Accident, id=accident_id)
    if not accident.is_deleted:
        accident.is_deleted = True
        accident.save()

        messages.success(request, 'Accident {accident.address} deleted successfully.')
        user = accident.created_by
        Message.objects.create(user=user, content=f"您的事故记录' '{accident.address}' 已被删除")

    return redirect('admin_dashboard')

def accident_detail(request, accident_id):
    accident = get_object_or_404(Accident, id=accident_id)
    return render(request, 'data/accident_detail.html', {'accident': accident})