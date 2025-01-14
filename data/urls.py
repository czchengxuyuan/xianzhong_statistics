from django.urls import path
from . import views

urlpatterns = [
    path('accident/create/', views.create_accident, name='accident_create'),
    path('accident/', views.accident_list, name='accident_list'),
    path('admin/review/', views.admin_review_accident, name='admin_review_accident'),
    path('admin/approve/<int:accident_id>/', views.approve_accident, name='admin_approve_accident'),
    path('admin/reject/<int:accident_id>/', views.reject_accident, name='admin_reject_accident'),
]
