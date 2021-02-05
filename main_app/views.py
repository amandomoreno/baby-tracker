from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Baby, Doctor, Photo
from .forms import FeedingForm, ChangingForm
import os
import uuid
import boto3
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'amandosbabyhub'

def home(request):
  return render(request, 'home.html')
  
def about(request):
    return render(request, 'about.html')

def babies_index(request):
    babies = Baby.objects.filter(user=request.user)
    return render(request, 'babies/index.html', { 'babies': babies })

@login_required
def babies_detail(request, baby_id):
  baby = Baby.objects.get(id=baby_id)
  doctors_baby_doesnt_have = Doctor.objects.exclude(id__in = baby.doctors.all().values_list('id'))
  feeding_form = FeedingForm()
  changing_form = ChangingForm()
  return render(request, 'babies/detail.html', { 'baby': baby, 'feeding_form': feeding_form, 'changing_form': changing_form, 'doctors': doctors_baby_doesnt_have
 })

@login_required
def add_feeding(request, baby_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.baby_id = baby_id
    new_feeding.save()
  return redirect('detail', baby_id=baby_id)

@login_required
def add_changing(request, baby_id):
  form = ChangingForm(request.POST)
  if form.is_valid():
    new_changing = form.save(commit=False)
    new_changing.baby_id = baby_id
    new_changing.save()
  return redirect('detail', baby_id=baby_id)

class BabyCreate(LoginRequiredMixin, CreateView):
  model = Baby
  fields = ['name', 'description', 'age']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class BabyUpdate(LoginRequiredMixin, UpdateView):
  model = Baby
  fields = ['name', 'description', 'age']

class BabyDelete(LoginRequiredMixin, DeleteView):
  model = Baby
  success_url = '/babies/'

class DoctorList(LoginRequiredMixin, ListView):
  model = Doctor

class DoctorDetail(LoginRequiredMixin, DetailView):
  model = Doctor

class DoctorCreate(LoginRequiredMixin, CreateView):
  model = Doctor
  fields = '__all__'

class DoctorUpdate(LoginRequiredMixin, UpdateView):
  model = Doctor
  fields = ['name', 'kind']

class DoctorDelete(LoginRequiredMixin, DeleteView):
  model = Doctor
  success_url = '/doctors/'

@login_required
def assoc_doctor(request, baby_id, doctor_id):
  Baby.objects.get(id=baby_id).doctors.add(doctor_id)
  return redirect('detail', baby_id=baby_id)

@login_required
def add_photo(request, baby_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, baby_id=baby_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', baby_id=baby_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def some_function(request):
    my_key = os.environ['SECRET_KEY']
