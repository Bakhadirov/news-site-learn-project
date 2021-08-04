from django.shortcuts import render
from .models import Rubric
# Create your views here.


def multilevelmenu(request):
    # return render(request, 'multilevelmenuapp/multilevelmenu.html') #рендерим по прежнему
    return render(request, "multilevelmenuapp/multilevelmenu.html", {'rubrics': Rubric.objects.all()})

def get_rubric(request):
    pass