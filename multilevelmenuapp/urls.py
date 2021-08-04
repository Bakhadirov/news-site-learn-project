from django.urls import path
from .views import *

urlpatterns = [
    path('', multilevelmenu, name = 'multilevelmenu'),
    path('rubric<int:pk>', get_rubric, name='rubric')

]