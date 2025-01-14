from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccidentForm
from .models import Accident
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

# Create your views here.

@login_required
def create_accident(request):
    if request.method == 'POST':
        form = AccidentForm(request.POST)
        if form.is_valid():
            accident = form.save(commit=False)
            accident.creted_by = request.user
            accident.is_approved = False
            accident.save()
            return redirect('accident_list')
    else:
        form = AccidentForm()
    return render(request, 'data/create_accident.html', {'form': form})

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
    accident.is_approved = True
    accident.save()
    return redirect('admin_review_accident')

@user_passes_test(is_admin)
def reject_accident(request, accident_id):
    accident = get_object_or_404(Accident, id=accident_id)
    accident.delete()
    return redirect('admin_review_accident')

def accident_detail(request, accident_id):
    accident = get_object_or_404(Accident, id=accident_id)
    return render(request, 'data/accident_detail.html', {'accident': accident})