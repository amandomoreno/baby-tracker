from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
import os

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Doctor(models.Model):
    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('doctors_detail', kwargs={'pk': self.id})

class Baby(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    age = models.IntegerField()
    doctors = models.ManyToManyField(Doctor)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'baby_id': self.id})

    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)
    
    class Meta:
        ordering = ['id']

class Feeding(models.Model):
  date = models.DateField('feeding date')
  meal = models.CharField(
    max_length=1,
    choices=MEALS,
    default=MEALS[0][0]
  )

  baby = models.ForeignKey(Baby, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_meal_display()} on {self.date}"

  class Meta:
    ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for baby_id: {self.baby_id} @{self.url}"

def some_function(request):
    my_key = os.environ['SECRET_KEY']