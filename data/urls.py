from django.urls import path
from . import views

urlpatterns = [
    path('accident/create/', views.create_accident, name='accident_create'),
    path('accident/', views.accident_list, name='accident_list'),
    path('review/', views.admin_review_accident, name='admin_review_accident'),
    path('approve/<int:accident_id>/', views.approve_accident, name='admin_approve_accident'),
    path('reject/<int:accident_id>/', views.reject_accident, name='admin_reject_accident'),
    path('delete/<int:accident_id>/', views.delete_accident, name='admin_delete_accident'),
    path('accident/<int:accident_id>/', views.accident_detail, name='accident_detail'),
    path('accident/<int:accident_id>/edit/', views.accident_edit, name='accident_edit'),
    path('userdelaci/<int:accident_id>/', views.accident_delete_user, name='accident_delete'),
    path('message/read/<int:message_id>/', views.mark_message_as_read, name='mark_message_as_read'),
]
