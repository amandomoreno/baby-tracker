from django.forms import ModelForm
from .models import Feeding
import os

class FeedingForm(ModelForm):
  class Meta:
    model = Feeding
    fields = ['date', 'meal']

def some_function(request):
    my_key = os.environ['SECRET_KEY']