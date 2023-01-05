from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm


def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0550a7a5b31a3b347ade188e121247e1'
    #city = 'Mumbai'

    err_msg = ''
    message = ''
    message_class =''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exists in the world!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

        #print(request.POST)
    print(err_msg)

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        # converts results into json objects
        r = requests.get(url.format(city)).json()
        # print(r.text)
        # CREATING A DICT THAT WILL REPRESENT ALL DATA OF MY APP INFORMATION
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],

        }

        weather_data.append(city_weather)
    
    #print(weather_data)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class,
        }
    #print(city_weather)

    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')

