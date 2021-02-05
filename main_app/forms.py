from django.forms import ModelForm
from .models import Feeding, Changing
import os

class FeedingForm(ModelForm):
  class Meta:
    model = Feeding
    fields = ['date', 'meal']

class ChangingForm(ModelForm):
  class Meta:
    model = Changing
    fields = ['date', 'diaper']

def some_function(request):
    my_key = os.environ['SECRET_KEY']