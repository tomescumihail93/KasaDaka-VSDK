from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from vsdk.api.serializers import UserSerializer, GroupSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Forecast, Region, Alert
from .serializers import ForecastSerializer, AlertSerializer
import urllib
import simplejson as json
from pprint import pprint
from datetime import datetime, timedelta

# Create your views here.

# forecasts/
class ForecastList(APIView):
    def get(self, request):
        forecasts = Forecast.objects.all()
        serializer = ForecastSerializer(forecasts, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self):
        pass

# forecasts/{region_id}/{day}
class ForecastDetail(APIView):
    def get(self, request, region_id, day):
        day = int(day)
        region = Region.objects.get(region_code=region_id)
        forecastDate = datetime.now()+timedelta(days=(day-1))
        #check if exists in database
        forecasts = Forecast.objects.filter(region=region, pub_date__year=forecastDate.year, pub_date__month=forecastDate.month, pub_date__day=forecastDate.day)
        if(len(forecasts) != 0):
            serializer = ForecastSerializer(forecasts, context={'request': request}, many=True)
            return Response(serializer.data)
        else:
            open_weather_response = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast?id='+ region_id +'&APPID=784a19283186fe17719114c8027ac5a7&units=metric').read().decode('UTF-8')
            weather_bit_response = urllib.request.urlopen('https://api.weatherbit.io/v2.0/forecast/3hourly?city_id='+ region_id +'&key=d4ab77bb12944aba96933f8f46724b49&units=metric').read().decode('UTF-8')
            OpenWeatherJson = json.loads(open_weather_response)
            WeatherBitJson = json.loads(weather_bit_response)
            parseOpenWeather(OpenWeatherJson, WeatherBitJson, region_id, forecastDate)
            forecast_resp = Forecast.objects.filter(region=region, pub_date__year=forecastDate.year, pub_date__month=forecastDate.month, pub_date__day=forecastDate.day)
            serializer = ForecastSerializer(forecast_resp, context={'request': request}, many=True)
            return Response(serializer.data)


# alerts/{region_id}
class AlertDetail(APIView):
    def get(self, request, region_id,):
        region = Region.objects.get(region_code=region_id)
        alertDate = datetime.now()
        alerts = Alert.objects.filter(region=region, pub_date__year=alertDate.year, pub_date__month=alertDate.month, pub_date__day=alertDate.day)
        # forecasts = Forecast.objects.all()
        serializer = AlertSerializer(alerts, context={'request': request}, many=True)
        return Response(serializer.data)

def parseOpenWeather(OpenWeatherJson, WeatherBitJson, region_id, forecastDate):
    region = Region.objects.get(region_code=region_id)
    reqForecast = Forecast()
    for i,val in enumerate(OpenWeatherJson['list']):
        if i % 8 == 0:
            openApiForecast = Forecast()
            openApiForecast.description = OpenWeatherJson['list'][i]['weather'][0]['description']
            openApiForecast.temperture = str(round((float(OpenWeatherJson['list'][i]['main']['temp']) + float(WeatherBitJson['data'][i]['app_temp']))/2, 2))
            openApiForecast.wind = str(round((float(OpenWeatherJson['list'][i]['wind']['speed']) + float(WeatherBitJson['data'][i]['wind_gust_spd']))/2, 2))
            openApiForecast.wind_angle = str(round((float(OpenWeatherJson['list'][i]['wind']['deg']) + float(WeatherBitJson['data'][i]['wind_dir']))/2, 2))
            openApiForecast.pub_date = datetime.strptime(OpenWeatherJson['list'][i]['dt_txt'], '%Y-%m-%d %H:%M:%S').date()
            openApiForecast.region = region
            openApiForecast.save()

# def parseWeatherBit(OpenWeatherJson, WeatherBitJson):
#     print("Hello WB!")
#     days = []
#     for i,val in enumerate(data['data']):
#         if i % 8 == 0:
#             openApiForecast = Forecast()
#             openApiForecast.description = WeatherBitJson['data'][i]['weather']['description']
#             openApiForecast.temperture = WeatherBitJson['data'][i]['app_temp']
#             openApiForecast.wind = WeatherBitJson['data'][i]['wind_gust_spd']
#             openApiForecast.wind_angle = WeatherBitJson['data'][i]['wind_dir']
#             openApiForecast.pub_date = datetime.datetime.strptime(data['data'][i]['datetime'], '%Y-%m-%d:%H').date()
#             days.append(openApiForecast)
#     return days

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer