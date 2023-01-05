
from django.urls import path
from . import views as v

urlpatterns = [
    
    path('', v.index, name='home'),
    path('delete/<city_name>/', v.delete_city, name='delete_city'),

]
