from django.urls import path
from . import views

urlpatterns = [
    path('accident/create/', views.create_accident, name='accident_create'),
    path('accident/', views.accident_list, name='accident_list'),
    path('review/', views.admin_review_accident, name='admin_review_accident'),
    path('approve/<int:accident_id>/', views.approve_accident, name='admin_approve_accident'),
    path('reject/<int:accident_id>/', views.reject_accident, name='admin_reject_accident'),
    path('accident/<int:accident_id>/', views.accident_detail, name='accident_detail'),
]
