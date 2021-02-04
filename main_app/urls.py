from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('babies/', views.babies_index, name='index'),
  path('babies/<int:baby_id>/', views.babies_detail, name='detail'),
  path('babies/create/', views.BabyCreate.as_view(), name='babies_create'),
  path('babies/<int:pk>/update/', views.BabyUpdate.as_view(), name='babies_update'),
  path('babies/<int:pk>/delete/', views.BabyDelete.as_view(), name='babies_delete'),
  path('babies/<int:baby_id>/add_feeding/', views.add_feeding, name='add_feeding'),

  path('doctors/', views.DoctorList.as_view(), name='doctors_index'),
  path('doctors/<int:pk>/', views.DoctorDetail.as_view(), name='doctors_detail'),
  path('doctors/create/', views.DoctorCreate.as_view(), name='doctors_create'),
  path('doctors/<int:pk>/update/', views.DoctorUpdate.as_view(), name='doctors_update'),
  path('doctors/<int:pk>/delete/', views.DoctorDelete.as_view(), name='doctors_delete'),
  path('doctors/<int:baby_id>/assoc_doctor/<int:doctor_id>/', views.assoc_doctor, name='assoc_doctor'),
  path('babies/<int:baby_id>/add_photo/', views.add_photo, name='add_photo'),
  path('accounts/signup/', views.signup, name='signup'),
]