from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'crop_advisory/',
        views.crop_advisory,
        name='crop_advisory'
    ),

    path(
        'pest_disease/',
        views.pest_disease,
        name='pest_disease'
    ),

    path(
        'farming_tips/',
        views.farming_tips,
        name='farming_tips'
    ),

    path(
        'livestock_advisory/',
        views.livestock_advisory,
        name='livestock_advisory'
    ),

    path(
        'about/',
        views.about,
        name='about'
    ),
    path(
        'feedback/',
        views.feedback,
        name='feedback'
        
    ),
    path(
            'logout/',
            views.logout_farmer,
            name='logout'
        ),
        path(
            'weather_calendar/', views.weather_calendar, name='weather_calendar'
        ),

    # Farmer Authentication

    path(
        'register/',
        views.register_farmer,
        name='register'
    ),

    path(
        'login/',
        views.login_farmer,
        name='login'
    ),
    path(
    'farmer-dashboard/',
    views.farmer_dashboard,
    name='farmer_dashboard'
),
    path(
    'chatbot/',
    views.chatbot,
    name='chatbot'
),



]
