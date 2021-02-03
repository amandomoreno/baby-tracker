from django.shortcuts import render
from django.http import HttpResponse

class Baby:  # Note that parens are optional if not inheriting from another class
  def __init__(self, name, description, age):
    self.name = name
    self.description = description
    self.age = age

babies = [
  Baby('Lolo', 'foul little demon', 3),
  Baby('Sachi', 'diluted tortoise shell', 0),
  Baby('Raven', '3 legged cat', 4)
]

def home(request):
  return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')

# def home(request):
#   return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def babies_index(request):
  return render(request, 'babies/index.html', { 'babies': babies })