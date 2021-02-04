from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Baby, Doctor, Photo
from .forms import FeedingForm
import os
import uuid
import boto3
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'amandosbabyhub'

def home(request):
  return render(request, 'home.html')
  
def about(request):
    return render(request, 'about.html')

def babies_index(request):
    babies = Baby.objects.all()
    return render(request, 'babies/index.html', { 'babies': babies })

def babies_detail(request, baby_id):
  baby = Baby.objects.get(id=baby_id)
  doctors_baby_doesnt_have = Doctor.objects.exclude(id__in = baby.doctors.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'babies/detail.html', { 'baby': baby, 'feeding_form': feeding_form, 'doctors': doctors_baby_doesnt_have
 })



def add_feeding(request, baby_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.baby_id = baby_id
    new_feeding.save()
  return redirect('detail', baby_id=baby_id)

class BabyCreate(CreateView):
  model = Baby
  fields = '__all__'

class BabyUpdate(UpdateView):
  model = Baby
  fields = ['name', 'description', 'age']

class BabyDelete(DeleteView):
  model = Baby
  success_url = '/babies/'

class DoctorList(ListView):
  model = Doctor

class DoctorDetail(DetailView):
  model = Doctor

class DoctorCreate(CreateView):
  model = Doctor
  fields = '__all__'

class DoctorUpdate(UpdateView):
  model = Doctor
  fields = ['name', 'kind']

class DoctorDelete(DeleteView):
  model = Doctor
  success_url = '/doctors/'

def assoc_doctor(request, baby_id, doctor_id):
  Baby.objects.get(id=baby_id).doctors.add(doctor_id)
  return redirect('detail', baby_id=baby_id)

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

def some_function(request):
    my_key = os.environ['SECRET_KEY']
