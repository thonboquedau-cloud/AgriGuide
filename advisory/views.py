from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.db.models import Q
from django.conf import settings

import requests
import re

from .forms import FarmerRegistrationForm, FeedbackForm
from .models import (
    CropAdvisory,
    PestDisease,
    FarmingTip,
    LivestockAdvisory,
    Feedback,
)


# ==========================================================
# HOME
# ==========================================================

def home(request):

    crops = CropAdvisory.objects.all()

    crop_count = CropAdvisory.objects.count()

    pest_count = PestDisease.objects.filter(
        problem_type__iexact="Pest"
    ).count()

    disease_count = PestDisease.objects.filter(
        problem_type__iexact="Disease"
    ).count()

    featured_crop = CropAdvisory.objects.order_by(
        "-created_at"
    ).first()

    featured_tip = FarmingTip.objects.order_by(
        "-created_at"
    ).first()

    featured_livestock = LivestockAdvisory.objects.order_by(
        "-created_at"
    ).first()

    animal_count = LivestockAdvisory.objects.count()

    return render(
        request,
        "advisory/home.html",
        {
            "crops": crops,
            "crop_count": crop_count,
            "pest_count": pest_count,
            "disease_count": disease_count,
            "featured_crop": featured_crop,
            "featured_tip": featured_tip,
            "featured_livestock": featured_livestock,
            "animal_count": animal_count,
        }
    )


# ==========================================================
# CROP ADVISORY
# ==========================================================

def crop_advisory(request):

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    selected_crop = request.GET.get(
        "crop",
        ""
    ).strip()

    if search_query:

        crops = CropAdvisory.objects.filter(
            crop_name__icontains=search_query
        )

    elif selected_crop:

        crops = CropAdvisory.objects.filter(
            crop_name__iexact=selected_crop
        )

    else:

        crops = CropAdvisory.objects.none()

    all_crops = CropAdvisory.objects.all().order_by(
        "crop_name"
    )

    pest_diseases = PestDisease.objects.all().order_by(
        "problem_name"
    )

    return render(
        request,
        "advisory/crop_advisory.html",
        {
            "crops": crops,
            "all_crops": all_crops,
            "search_query": search_query,
            "selected_crop": selected_crop,
            "pest_diseases": pest_diseases,
        }
    )


# ==========================================================
# PEST AND DISEASE
# ==========================================================

def pest_disease(request):

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    selected_crop = request.GET.get(
        "crop",
        ""
    ).strip()

    if search_query:

        problems = PestDisease.objects.filter(
            problem_name__icontains=search_query
        )

    elif selected_crop:

        problems = PestDisease.objects.filter(
            crop_name__iexact=selected_crop
        )

    else:

        problems = PestDisease.objects.none()

    all_crops = PestDisease.objects.values_list(
        "crop_name",
        flat=True
    ).distinct().order_by(
        "crop_name"
    )

    return render(
        request,
        "advisory/pest_disease.html",
        {
            "problems": problems,
            "all_crops": all_crops,
            "search_query": search_query,
            "selected_crop": selected_crop,
        }
    )


# ==========================================================
# FARMING TIPS
# ==========================================================

def farming_tips(request):

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    if search_query:

        tips = FarmingTip.objects.filter(
            title__icontains=search_query
        )

    else:

        tips = FarmingTip.objects.all().order_by(
            "-created_at"
        )

    return render(
        request,
        "advisory/farming_tips.html",
        {
            "tips": tips,
            "search_query": search_query,
        }
    )


# ==========================================================
# LIVESTOCK ADVISORY
# ==========================================================

def livestock_advisory(request):

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    selected_animal = request.GET.get(
        "animal",
        ""
    ).strip()

    if search_query:

        animals = LivestockAdvisory.objects.filter(
            animal_name__icontains=search_query
        )

    elif selected_animal:

        animals = LivestockAdvisory.objects.filter(
            animal_name__iexact=selected_animal
        )

    else:

        animals = LivestockAdvisory.objects.none()

    all_animals = LivestockAdvisory.objects.all().order_by(
        "animal_name"
    )

    return render(
        request,
        "advisory/livestock_advisory.html",
        {
            "animals": animals,
            "all_animals": all_animals,
            "search_query": search_query,
            "selected_animal": selected_animal,
        }
    )


# ==========================================================
# ABOUT
# ==========================================================

def about(request):

    return render(
        request,
        "advisory/about.html"
    )


# ==========================================================
# FEEDBACK
# ==========================================================

def feedback(request):

    if request.method == "POST":

        form = FeedbackForm(request.POST)

        if form.is_valid():

            form.save()

            return render(
                request,
                "advisory/feedback.html",
                {
                    "form": FeedbackForm(),
                    "success": (
                        "Thank you! Your feedback has been "
                        "submitted successfully."
                    )
                }
            )

    else:

        form = FeedbackForm()

    return render(
        request,
        "advisory/feedback.html",
        {
            "form": form
        }
    )


# ==========================================================
# FARMER REGISTRATION
# ==========================================================

def register_farmer(request):

    if request.user.is_authenticated:

        return redirect("home")

    if request.method == "POST":

        form = FarmerRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            return redirect(
                "farmer_dashboard"
            )

    else:

        form = FarmerRegistrationForm()

    return render(
        request,
        "advisory/register.html",
        {
            "form": form
        }
    )


# ==========================================================
# FARMER LOGIN
# ==========================================================

def login_farmer(request):

    if request.user.is_authenticated:

        return redirect(
            "farmer_dashboard"
        )

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect(
                "farmer_dashboard"
            )

        return render(
            request,
            "advisory/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "advisory/login.html"
    )


# ==========================================================
# FARMER DASHBOARD
# ==========================================================

def farmer_dashboard(request):

    if not request.user.is_authenticated:

        return redirect("login")

    crop_count = CropAdvisory.objects.count()

    animal_count = LivestockAdvisory.objects.count()

    pest_count = PestDisease.objects.filter(
        problem_type__iexact="Pest"
    ).count()

    disease_count = PestDisease.objects.filter(
        problem_type__iexact="Disease"
    ).count()

    farming_tip_count = FarmingTip.objects.count()

    return render(
        request,
        "advisory/farmer_dashboard.html",
        {
            "crop_count": crop_count,
            "animal_count": animal_count,
            "pest_count": pest_count,
            "disease_count": disease_count,
            "farming_tip_count": farming_tip_count,
        }
    )


# ==========================================================
# LOGOUT
# ==========================================================

def logout_farmer(request):

    logout(request)

    return redirect("home")


# ==========================================================
# WEATHER, REAL-TIME FARMER INFORMATION
# AND FARMING CALENDAR
# ==========================================================

def weather_calendar(request):

    api_key = settings.OPENWEATHER_API_KEY

    weather_url = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    forecast_url = (
        "https://api.openweathermap.org/data/2.5/forecast"
    )

    params = {
        "q": "Juba,SS",
        "appid": api_key,
        "units": "metric",
    }

    weather = None
    forecast = None
    error = None

    # ==========================================================
    # REAL-TIME FARMER ADVISORY VARIABLES
    # ==========================================================

    farmer_alerts = []

    farmer_summary = (
        "Live weather conditions are being monitored "
        "for farming guidance in Juba."
    )

    try:

        # ======================================================
        # CURRENT WEATHER
        # ======================================================

        weather_response = requests.get(
            weather_url,
            params=params,
            timeout=10
        )

        # ======================================================
        # WEATHER FORECAST
        # ======================================================

        forecast_response = requests.get(
            forecast_url,
            params=params,
            timeout=10
        )

        if weather_response.status_code == 200:

            weather = weather_response.json()

        else:

            error = (
                "Unable to retrieve current "
                "weather information."
            )

        if forecast_response.status_code == 200:

            forecast_data = forecast_response.json()

            forecast = forecast_data.get(
                "list",
                []
            )[:8]

        else:

            error = (
                "Unable to retrieve forecast "
                "information."
            )

    except requests.exceptions.RequestException:

        error = (
            "Weather service is currently unavailable."
        )

    # ==========================================================
    # REAL-TIME FARMER INTERPRETATION
    # ==========================================================

    if weather:

        try:

            temperature = float(
                weather.get(
                    "main",
                    {}
                ).get(
                    "temp",
                    0
                )
            )

            humidity = float(
                weather.get(
                    "main",
                    {}
                ).get(
                    "humidity",
                    0
                )
            )

            wind_speed = float(
                weather.get(
                    "wind",
                    {}
                ).get(
                    "speed",
                    0
                )
            )

            weather_condition = (
                weather.get(
                    "weather",
                    [{}]
                )[0].get(
                    "main",
                    ""
                ).lower()
            )

            weather_description = (
                weather.get(
                    "weather",
                    [{}]
                )[0].get(
                    "description",
                    ""
                ).lower()
            )

            # ==================================================
            # RAIN CONDITIONS
            # ==================================================

            if (
                "rain" in weather_condition
                or "drizzle" in weather_condition
                or "thunderstorm" in weather_condition
            ):

                farmer_alerts.append(
                    {
                        "type": "rain",
                        "icon": "🌧️",
                        "title": "Rain Alert",
                        "message": (
                            "Rain or wet conditions are currently "
                            "being reported. Where practical, farmers "
                            "should avoid spraying pesticides or "
                            "fertilizers immediately before or during "
                            "heavy rainfall because rain may reduce "
                            "their effectiveness."
                        )
                    }
                )

            # ==================================================
            # HIGH TEMPERATURE
            # ==================================================

            if temperature >= 35:

                farmer_alerts.append(
                    {
                        "type": "heat",
                        "icon": "🌡️",
                        "title": "High Temperature Alert",
                        "message": (
                            "High temperatures are currently being "
                            "reported. Monitor crops for water stress "
                            "and provide livestock with adequate clean "
                            "drinking water and shade where possible."
                        )
                    }
                )

            elif temperature >= 32:

                farmer_alerts.append(
                    {
                        "type": "warm",
                        "icon": "☀️",
                        "title": "Warm Conditions",
                        "message": (
                            "Warm conditions are currently being "
                            "reported. Farmers should monitor soil "
                            "moisture and livestock water availability, "
                            "especially during dry periods."
                        )
                    }
                )

            # ==================================================
            # HIGH HUMIDITY
            # ==================================================

            if humidity >= 80:

                farmer_alerts.append(
                    {
                        "type": "humidity",
                        "icon": "💧",
                        "title": "High Humidity Alert",
                        "message": (
                            "Humidity is currently high. Farmers should "
                            "inspect crops regularly for signs of fungal "
                            "or other moisture-related diseases and "
                            "maintain good field ventilation and hygiene."
                        )
                    }
                )

            # ==================================================
            # STRONG WIND
            # ==================================================

            if wind_speed >= 8:

                farmer_alerts.append(
                    {
                        "type": "wind",
                        "icon": "💨",
                        "title": "Strong Wind Alert",
                        "message": (
                            "Strong winds are currently being reported. "
                            "Avoid spraying agricultural chemicals when "
                            "wind conditions could cause spray drift and "
                            "take care when working with exposed crops "
                            "or equipment."
                        )
                    }
                )

            # ==================================================
            # CLEAR / DRY CONDITIONS
            # ==================================================

            if (
                weather_condition in (
                    "clear",
                    "clouds"
                )
                and humidity < 60
                and temperature >= 30
            ):

                farmer_alerts.append(
                    {
                        "type": "dry",
                        "icon": "☀️",
                        "title": "Dry Conditions",
                        "message": (
                            "Current conditions are relatively warm and "
                            "dry. Farmers should monitor soil moisture, "
                            "reduce unnecessary water loss and use "
                            "available water efficiently."
                        )
                    }
                )

            # ==================================================
            # GENERAL FARMING SUMMARY
            # ==================================================

            if (
                "rain" in weather_condition
                or "drizzle" in weather_condition
            ):

                farmer_summary = (
                    "Wet conditions are currently being reported. "
                    "Farmers should monitor rainfall and field "
                    "conditions before carrying out field operations."
                )

            elif (
                "thunderstorm" in weather_condition
            ):

                farmer_summary = (
                    "Thunderstorm conditions are currently being "
                    "reported. Farmers should take precautions and "
                    "avoid unnecessary exposure to severe weather."
                )

            elif temperature >= 35:

                farmer_summary = (
                    "Hot conditions are currently being reported. "
                    "Monitor crops, livestock and water availability "
                    "carefully."
                )

            elif temperature >= 32:

                farmer_summary = (
                    "Warm conditions are currently being reported. "
                    "Monitor soil moisture, crops and livestock water "
                    "availability."
                )

            else:

                farmer_summary = (
                    "Current weather conditions are being monitored "
                    "for practical farming decisions in Juba."
                )

            # ==================================================
            # FORECAST-BASED ALERT
            # ==================================================

            if forecast:

                rain_expected = False
                heavy_rain_expected = False

                for forecast_item in forecast:

                    forecast_weather = (
                        forecast_item.get(
                            "weather",
                            [{}]
                        )[0].get(
                            "main",
                            ""
                        ).lower()
                    )

                    forecast_description = (
                        forecast_item.get(
                            "weather",
                            [{}]
                        )[0].get(
                            "description",
                            ""
                        ).lower()
                    )

                    if (
                        "rain" in forecast_weather
                        or "drizzle" in forecast_weather
                        or "rain" in forecast_description
                    ):

                        rain_expected = True

                    if (
                        "thunderstorm" in forecast_weather
                        or "heavy rain" in forecast_description
                    ):

                        heavy_rain_expected = True

                if heavy_rain_expected:

                    farmer_alerts.append(
                        {
                            "type": "forecast",
                            "icon": "⛈️",
                            "title": "Forecast Rainfall Alert",
                            "message": (
                                "Rain or thunderstorms appear in the "
                                "available short-term forecast. Farmers "
                                "should monitor field conditions and "
                                "consider rainfall when planning "
                                "spraying, fertilizer application, "
                                "harvesting or other field activities."
                            )
                        }
                    )

                elif rain_expected:

                    farmer_alerts.append(
                        {
                            "type": "forecast",
                            "icon": "🌦️",
                            "title": "Rain in Short-Term Forecast",
                            "message": (
                                "Rain is indicated in the available "
                                "short-term forecast. Farmers should "
                                "check the forecast before scheduling "
                                "weather-sensitive farm activities."
                            )
                        }
                    )

        except (
            TypeError,
            ValueError,
            IndexError,
            KeyError
        ):

            farmer_alerts = []

            farmer_summary = (
                "Current weather data is available, but some "
                "farmer-specific interpretation could not be "
                "calculated."
            )

    # ==========================================================
    # FARMING CALENDAR
    # ==========================================================

    farming_calendar = [

        {
            "month": "January",
            "activity": "☀️ Dry-season farming",
            "advice": (
                "Focus on irrigation where available, "
                "livestock management, soil conservation "
                "and preparation of land for the coming "
                "rainy season."
            )
        },

        {
            "month": "February",
            "activity": "🌱 Land preparation",
            "advice": (
                "Clear and prepare fields, repair farm "
                "tools and begin planning crops and seeds "
                "for the rainy season."
            )
        },

        {
            "month": "March",
            "activity": "🌱 Land preparation and seed selection",
            "advice": (
                "Select quality seeds, prepare planting "
                "areas and improve soil fertility using "
                "available organic materials."
            )
        },

        {
            "month": "April",
            "activity": "🌧️ Prepare for planting",
            "advice": (
                "Monitor the beginning of rainfall, "
                "complete land preparation and prepare "
                "seeds and planting materials."
            )
        },

        {
            "month": "May",
            "activity": "🌱 Planting season",
            "advice": (
                "Plant suitable crops when sufficient "
                "rainfall has established good soil "
                "moisture. Begin early weed and pest "
                "monitoring."
            )
        },

        {
            "month": "June",
            "activity": "🌿 Crop establishment",
            "advice": (
                "Control weeds, monitor crop growth and "
                "apply appropriate fertilizer or organic "
                "manure where needed."
            )
        },

        {
            "month": "July",
            "activity": "🐛 Pest and disease monitoring",
            "advice": (
                "Regularly inspect crops for pests and "
                "diseases. Use integrated pest management "
                "practices and maintain good field hygiene."
            )
        },

        {
            "month": "August",
            "activity": "🌿 Weeding and crop management",
            "advice": (
                "Continue effective weed management, "
                "monitor pests and diseases, and maintain "
                "adequate soil moisture."
            )
        },

        {
            "month": "September",
            "activity": "🌾 Crop maturity",
            "advice": (
                "Monitor crops as they mature, protect "
                "them from pests and diseases, and prepare "
                "storage facilities and harvesting tools."
            )
        },

        {
            "month": "October",
            "activity": "🌾 Harvesting",
            "advice": (
                "Harvest mature crops at the appropriate "
                "time, dry produce properly and store it "
                "safely to reduce post-harvest losses."
            )
        },

        {
            "month": "November",
            "activity": "🌾 Post-harvest management",
            "advice": (
                "Clean and store harvested produce properly. "
                "Preserve seeds for the next season and "
                "begin planning future farm activities."
            )
        },

        {
            "month": "December",
            "activity": "🌱 Farm planning",
            "advice": (
                "Review the farming season, maintain "
                "equipment, manage livestock and prepare "
                "plans for the next agricultural season."
            )
        },
    ]

    # ==========================================================
    # RENDER WEATHER PAGE
    # ==========================================================

    return render(
        request,
        "advisory/weather_calendar.html",
        {
            "weather": weather,
            "forecast": forecast,
            "error": error,
            "farming_calendar": farming_calendar,

            # Real-time farmer information
            "farmer_alerts": farmer_alerts,
            "farmer_summary": farmer_summary,
        }
    )
# ==========================================================
# CATTLE HELPER
# ==========================================================

def _get_cattle_advisory():

    return LivestockAdvisory.objects.filter(
        Q(animal_name__icontains="cattle")
        | Q(animal_name__icontains="cow")
        | Q(animal_category__icontains="large livestock")
    ).distinct().first()


# ==========================================================
# AGRIGUIDE CHATBOT
# ==========================================================

def chatbot(request):
    answer = None
    question = ""

    # These are filled in once a question is received.
    clean_q = ""
    words = set()

    # ==========================================================
    # STOP WORDS
    # Used when searching the AgriGuide knowledge base
    # ==========================================================

    stop_words = {
        "how",
        "what",
        "where",
        "when",
        "why",
        "which",
        "who",
        "can",
        "do",
        "does",
        "did",
        "is",
        "are",
        "am",
        "the",
        "a",
        "an",
        "to",
        "of",
        "for",
        "in",
        "on",
        "with",
        "and",
        "or",
        "my",
        "i",
        "me",
        "about",
        "tell",
        "give",
        "please",
        "should",
        "could",
        "would",
        "you",
        "your",
        "we",
        "our",
        "it",
        "this",
        "that",
        "be",
        "best",
        "some",
        "any",
        "show",
        "crop",
        "crops",
        "plant",
        "plants",
        "farm",
        "farming",
        "farmer",
        "farmers",
        "information",
        "info",
        "advice",
    }

    # ==========================================================
    # BASIC HELPER
    # ==========================================================

    def _has(*terms):
        """
        Returns True when one of the supplied words or phrases
        appears in the cleaned question.
        """

        for term in terms:

            term = term.lower().strip()

            if " " in term:

                if term in clean_q:
                    return True

            else:

                if term in words:
                    return True

        return False

    # ==========================================================
    # CATTLE HELPERS
    # ==========================================================

    def _is_cattle():
        return _has(
            "cattle",
            "cow",
            "cows"
        )

    def _get_cattle_advisory():

        try:

            return (
                LivestockAdvisory.objects
                .filter(
                    Q(animal_name__icontains="cattle")
                    | Q(animal_name__icontains="cow")
                    | Q(category__icontains="large livestock")
                )
                .distinct()
                .first()
            )

        except Exception:

            return None

    # ==========================================================
    # CROP ADVISORY HELPER
    # ==========================================================

    def _get_crop_advisory(crop_terms):

        query = Q()

        for term in crop_terms:

            query |= Q(
                crop_name__icontains=term
            )

        try:

            return (
                CropAdvisory.objects
                .filter(query)
                .distinct()
                .first()
            )

        except Exception:

            return None

    # ==========================================================
    # PEST / DISEASE HELPER
    # ==========================================================

    def _get_crop_problems(crop_terms, problem_type=None):

        crop_query = Q()

        for term in crop_terms:

            crop_query |= Q(
                crop_name__icontains=term
            )

        try:

            queryset = PestDisease.objects.filter(
                crop_query
            )

            if problem_type:

                queryset = queryset.filter(
                    problem_type__iexact=problem_type
                )

            return queryset.distinct()

        except Exception:

            return PestDisease.objects.none()

    # ==========================================================
    # SYMPTOM GROUPS
    # ==========================================================

    symptom_groups = {

        "yellowing": {
            "words": {
                "yellow",
                "yellowing",
                "pale",
                "paling"
            },
            "phrases": {
                "leaves turning yellow",
                "leaves are yellow",
                "yellow leaves",
                "yellow leaves on",
                "yellowing leaves",
                "leaf yellowing",
                "leaves becoming yellow",
                "leaves becoming pale",
                "pale leaves"
            }
        },

        "streaks": {
            "words": {
                "streak",
                "streaks",
                "stripe",
                "stripes"
            },
            "phrases": {
                "yellow streaks",
                "yellow stripes",
                "pale streaks",
                "pale stripes",
                "streaks on leaves",
                "stripes on leaves"
            }
        },

        "spots": {
            "words": {
                "spot",
                "spots",
                "lesion",
                "lesions"
            },
            "phrases": {
                "brown spots",
                "black spots",
                "white spots",
                "yellow spots",
                "spots on leaves",
                "spots on the leaves",
                "leaf spots"
            }
        },

        "wilting": {
            "words": {
                "wilt",
                "wilting",
                "drooping",
                "droop"
            },
            "phrases": {
                "leaves are wilting",
                "leaves wilting",
                "plant is wilting",
                "plants are wilting",
                "leaves are drooping",
                "plant is drooping"
            }
        },

        "drying": {
            "words": {
                "dry",
                "drying",
                "dried",
                "dryness"
            },
            "phrases": {
                "leaves are drying",
                "leaves drying",
                "plant is drying",
                "plants are drying",
                "crop is drying"
            }
        },

        "holes": {
            "words": {
                "hole",
                "holes",
                "chewed",
                "chewing",
                "eaten",
                "eating"
            },
            "phrases": {
                "holes in leaves",
                "holes on leaves",
                "leaves have holes",
                "leaves are being eaten",
                "leaves being eaten",
                "leaves are chewed",
                "leaves being chewed"
            }
        },

        "insects": {
            "words": {
                "insect",
                "insects",
                "bug",
                "bugs",
                "pest",
                "pests",
                "worm",
                "worms",
                "caterpillar",
                "caterpillars",
                "armyworm",
                "armyworms",
                "borer",
                "borers",
                "fly",
                "flies",
                "beetle",
                "beetles",
                "aphid",
                "aphids"
            },
            "phrases": {
                "insect attack",
                "pest attack",
                "pest damage",
                "insect damage",
                "insects attacking",
                "pests attacking"
            }
        },

        "stunting": {
            "words": {
                "stunted",
                "stunting",
                "stunt",
                "small",
                "weak",
                "growth"
            },
            "phrases": {
                "stunted growth",
                "poor growth",
                "slow growth",
                "plants not growing",
                "crop not growing",
                "poor plant growth"
            }
        },

        "rotting": {
            "words": {
                "rot",
                "rotting",
                "rotten",
                "decay",
                "decaying"
            },
            "phrases": {
                "root rot",
                "rotting roots",
                "roots are rotting",
                "root is rotting",
                "crop is rotting",
                "plant is rotting"
            }
        },

        "curling": {
            "words": {
                "curl",
                "curling",
                "curled",
                "twisted",
                "twisting"
            },
            "phrases": {
                "curled leaves",
                "leaves curling",
                "leaves are curling",
                "leaves have curled",
                "leaf curling",
                "twisted leaves"
            }
        },

        "browning": {
            "words": {
                "brown",
                "browning",
                "black",
                "blackening"
            },
            "phrases": {
                "leaves turning brown",
                "brown leaves",
                "leaves are brown",
                "leaf browning",
                "black leaves"
            }
        },

        "mosaic": {
            "words": {
                "mosaic",
                "mottled",
                "mottle"
            },
            "phrases": {
                "mosaic pattern",
                "mosaic symptoms",
                "mottled leaves",
                "mottled leaf pattern"
            }
        },
    }

    # ==========================================================
    # DETECT SYMPTOMS
    # ==========================================================

    def _detect_symptoms():

        detected = []

        for symptom, data in symptom_groups.items():

            found = False

            for word in data["words"]:

                if word in words:

                    found = True
                    break

            if not found:

                for phrase in data["phrases"]:

                    if phrase in clean_q:

                        found = True
                        break

            if found:

                detected.append(symptom)

        return detected

    # ==========================================================
    # SYMPTOM IDENTIFICATION QUESTION
    # ==========================================================

    def _is_symptom_identification_question():

        detected = _detect_symptoms()

        if detected:

            return True

        identification_phrases = (
            "what is wrong",
            "what is affecting",
            "what is affecting my crop",
            "what is affecting the crop",
            "what disease is this",
            "what pest is this",
            "what is this disease",
            "what is this pest",
            "what is this insect",
            "what could be responsible",
            "what could be causing",
            "what is causing",
            "why are my leaves",
            "why is my crop",
            "my crop is sick",
            "my plant is sick",
            "what happened to my crop",
            "what happened to my plant"
        )

        return any(
            phrase in clean_q
            for phrase in identification_phrases
        )

    # ==========================================================
    # SYMPTOM MATCHING
    # ==========================================================

    def _symptom_matches(crop_terms):

        detected = _detect_symptoms()

        # ------------------------------------------------------
        # IMPORTANT:
        # If the farmer clearly asks about a pest, do not mix
        # unrelated diseases into the results.
        # ------------------------------------------------------

        wants_pest = _wants_pest()
        wants_disease = _wants_disease()

        if wants_pest and not wants_disease:

            problems = _get_crop_problems(
                crop_terms,
                problem_type="Pest"
            )

        elif wants_disease and not wants_pest:

            problems = _get_crop_problems(
                crop_terms,
                problem_type="Disease"
            )

        else:

            problems = _get_crop_problems(
                crop_terms
            )

        important_phrases = {

            "yellowing": [
                "yellow leaves",
                "leaves turning yellow",
                "yellowing leaves"
            ],

            "streaks": [
                "yellow streaks",
                "yellow stripes",
                "pale streaks",
                "pale stripes"
            ],

            "spots": [
                "brown spots",
                "black spots",
                "white spots",
                "yellow spots",
                "spots on leaves"
            ],

            "holes": [
                "holes in leaves",
                "holes on leaves",
                "leaves have holes",
                "leaves are being eaten",
                "leaves are chewed"
            ],

            "wilting": [
                "leaves are wilting",
                "plant is wilting",
                "leaves are drooping"
            ],

            "drying": [
                "leaves are drying",
                "plant is drying",
                "crop is drying"
            ],

            "stunting": [
                "stunted growth",
                "poor growth",
                "slow growth",
                "plants not growing"
            ],

            "rotting": [
                "root rot",
                "rotting roots",
                "roots are rotting"
            ],

            "curling": [
                "curled leaves",
                "leaves curling",
                "leaves are curling"
            ],

            "mosaic": [
                "mosaic pattern",
                "mottled leaves"
            ]
        }

        matches = []

        for problem in problems:

            score = 0

            problem_name = (
                getattr(
                    problem,
                    "problem_name",
                    ""
                ) or ""
            ).lower()

            symptoms_text = (
                getattr(
                    problem,
                    "symptoms",
                    ""
                ) or ""
            ).lower()

            causes_text = (
                getattr(
                    problem,
                    "causes",
                    ""
                ) or ""
            ).lower()

            prevention_text = (
                getattr(
                    problem,
                    "prevention",
                    ""
                ) or ""
            ).lower()

            control_text = (
                getattr(
                    problem,
                    "control_measures",
                    ""
                ) or ""
            ).lower()

            observed_text = (
                getattr(
                    problem,
                    "observed_symptoms",
                    ""
                ) or ""
            ).lower()

            combined_text = " ".join(
                [
                    problem_name,
                    symptoms_text,
                    causes_text,
                    prevention_text,
                    control_text,
                    observed_text,
                ]
            )

            # --------------------------------------------------
            # SCORE DETECTED SYMPTOMS
            # --------------------------------------------------

            for symptom in detected:

                symptom_data = symptom_groups.get(
                    symptom,
                    {}
                )

                for word in symptom_data.get(
                    "words",
                    set()
                ):

                    if word in combined_text:

                        score += 2

                for phrase in symptom_data.get(
                    "phrases",
                    set()
                ):

                    if phrase in combined_text:

                        score += 4

                for phrase in important_phrases.get(
                    symptom,
                    []
                ):

                    if phrase in combined_text:

                        score += 5

            # --------------------------------------------------
            # QUESTION WORD MATCHING
            # --------------------------------------------------

            question_words = set(
                clean_q.split()
            ) - stop_words

            for word in question_words:

                if len(word) < 3:
                    continue

                if word in problem_name:

                    score += 5

                if word in symptoms_text:

                    score += 2

                if word in causes_text:

                    score += 1

            # --------------------------------------------------
            # PROBLEM NAME RELEVANCE
            # --------------------------------------------------

            for word in words:

                if len(word) >= 4 and word in problem_name:

                    score += 3

            if score > 0:

                matches.append(
                    (
                        score,
                        problem
                    )
                )

        matches.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return matches

    # ==========================================================
    # SYMPTOM FOLLOW-UP
    # ==========================================================

    def _symptom_follow_up(
        crop_title,
        detected,
        matches
    ):

        if "yellowing" in detected:

            return (
                f"Because your {crop_title.lower()} leaves are yellowing, "
                "check whether the yellowing starts from older or younger "
                "leaves, whether the veins remain green, and whether the "
                "soil is waterlogged or too dry."
            )

        if "holes" in detected or "insects" in detected:

            return (
                f"Because your {crop_title.lower()} has chewing damage, "
                "inspect the leaves and growing points for caterpillars, "
                "worms, beetles, eggs, or insect droppings. If possible, "
                "take a clear photo of the pest and the damaged leaves."
            )

        if "wilting" in detected:

            return (
                f"Because your {crop_title.lower()} is wilting, "
                "check soil moisture, root condition, drainage, and the "
                "presence of insects or disease symptoms."
            )

        if "spots" in detected:

            return (
                f"Because your {crop_title.lower()} has leaf spots, "
                "check the colour, shape, size, and pattern of the spots "
                "and whether they are spreading to new leaves."
            )

        if "stunting" in detected:

            return (
                f"Because your {crop_title.lower()} has poor or stunted "
                "growth, check soil fertility, moisture, spacing, weeds, "
                "pests, and possible disease symptoms."
            )

        return (
            "For a more accurate AgriGuide match, tell me the crop, "
            "the main symptom, when it started, and whether the problem "
            "is spreading."
        )

    # ==========================================================
    # SHOW SYMPTOM MATCHES
    # ==========================================================

    def _show_symptom_matches(
        crop_terms,
        crop_title,
        icon
    ):

        detected = _detect_symptoms()

        matches = _symptom_matches(
            crop_terms
        )

        if not matches:

            return (
                f"{icon} <b>{crop_title} Health Check</b><br><br>"
                "I could not find a strong matching problem in the "
                "AgriGuide knowledge base.<br><br>"
                "Please provide more information such as:<br>"
                "• What part of the plant is affected?<br>"
                "• What colour are the symptoms?<br>"
                "• Are there holes, spots, streaks, wilting or curling?<br>"
                "• Are insects, worms or caterpillars visible?<br>"
                "• Is the problem spreading?<br><br>"
                "If possible, provide a clear photo for human or expert "
                "inspection."
            )

        response = (
            f"{icon} <b>Possible {crop_title} Health Problems</b><br><br>"
        )

        response += (
            "<i>AgriGuide provides a database-based advisory match. "
            "This is not a laboratory diagnosis.</i><br><br>"
        )

        if detected:

            response += (
                "<b>Symptoms detected from your question:</b> "
                + ", ".join(
                    detected
                )
                + "<br><br>"
            )

        response += (
            "<b>Possible matching problems:</b><br><br>"
        )

        for index, item in enumerate(
            matches[:5],
            start=1
        ):

            score, problem = item

            problem_name = (
                getattr(
                    problem,
                    "problem_name",
                    "Unknown problem"
                )
                or "Unknown problem"
            )

            problem_type = (
                getattr(
                    problem,
                    "problem_type",
                    ""
                )
                or ""
            )

            symptoms = (
                getattr(
                    problem,
                    "symptoms",
                    ""
                )
                or ""
            )

            causes = (
                getattr(
                    problem,
                    "causes",
                    ""
                )
                or ""
            )

            prevention = (
                getattr(
                    problem,
                    "prevention",
                    ""
                )
                or ""
            )

            control = (
                getattr(
                    problem,
                    "control_measures",
                    ""
                )
                or ""
            )

            response += (
                f"<b>{index}. {problem_name}</b>"
                f" ({problem_type})<br>"
            )

            if score >= 10:

                response += (
                    "<b>Match strength:</b> Strong<br>"
                )

            elif score >= 5:

                response += (
                    "<b>Match strength:</b> Moderate<br>"
                )

            else:

                response += (
                    "<b>Match strength:</b> Possible<br>"
                )

            if symptoms:

                response += (
                    f"<b>Symptoms:</b> {symptoms}<br>"
                )

            if causes:

                response += (
                    f"<b>Possible causes:</b> {causes}<br>"
                )

            if prevention:

                response += (
                    f"<b>Prevention:</b> {prevention}<br>"
                )

            if control:

                response += (
                    f"<b>Control measures:</b> {control}<br>"
                )

            response += "<br>"

        response += (
            "<b>Further checking:</b><br>"
            + _symptom_follow_up(
                crop_title,
                detected,
                matches
            )
            + "<br><br>"
        )

        response += (
            "<b>You can also ask:</b><br>"
            f"• What causes disease in {crop_title.lower()}?<br>"
            f"• How can I prevent {crop_title.lower()} diseases?<br>"
            f"• What pests attack {crop_title.lower()}?<br>"
            f"• How can I control pests on {crop_title.lower()}?"
        )

        return response

    # ==========================================================
    # DISEASE INTENT
    # ==========================================================

    def _wants_disease():

        disease_terms = (
            "disease",
            "diseases",
            "sick",
            "illness",
            "infection",
            "infections",
            "symptom",
            "symptoms",
            "what is wrong",
            "what is affecting",
            "yellow leaves",
            "yellowing leaves",
            "yellow streaks",
            "yellow stripes",
            "brown spots",
            "black spots",
            "white spots",
            "wilting",
            "rotting",
            "root rot",
            "mosaic"
        )

        return any(
            term in clean_q
            for term in disease_terms
        )

    # ==========================================================
    # PEST INTENT
    # ==========================================================

    def _wants_pest():

        pest_terms = (
            "pest",
            "pests",
            "insect",
            "insects",
            "bug",
            "bugs",
            "worm",
            "worms",
            "caterpillar",
            "caterpillars",
            "armyworm",
            "armyworms",
            "borer",
            "borers",
            "fly",
            "flies",
            "beetle",
            "beetles",
            "aphid",
            "aphids",
            "damage",
            "eating",
            "eaten",
            "holes",
            "chewed",
            "chewing"
        )

        return any(
            term in clean_q
            for term in pest_terms
        )

    # ==========================================================
    # QUESTION FOCUS
    # ==========================================================

    def _focuses_from_question():

        focus = set()

        if _has(
            "symptom",
            "symptoms",
            "sign",
            "signs",
            "what does it look like"
        ):

            focus.add("symptoms")

        if _has(
            "cause",
            "causes",
            "causing",
            "why",
            "reason"
        ):

            focus.add("causes")

        if _has(
            "prevent",
            "prevention",
            "protect",
            "avoid"
        ):

            focus.add("prevention")

        if _has(
            "control",
            "treat",
            "treatment",
            "manage",
            "management",
            "get rid",
            "reduce"
        ):

            focus.add("control")

        if not focus:

            focus.add("all")

        return focus

    # ==========================================================
    # REQUESTED CROP TOPICS
    # ==========================================================

    def _requested_topics():

        topics = []

        if _has(
            "soil",
            "soil type",
            "soil conditions"
        ):

            topics.append(
                (
                    "Recommended Soil",
                    "soil_type"
                )
            )

        if _has(
            "planting season",
            "when to plant",
            "best time to plant",
            "planting time",
            "season to plant"
        ):

            topics.append(
                (
                    "Planting Season",
                    "planting_season"
                )
            )

        elif _has(
            "plant",
            "planting",
            "sow",
            "sowing",
            "cultivate",
            "cultivation",
            "grow",
            "growing",
            "how to plant"
        ):

            topics.append(
                (
                    "Planting Advice",
                    "planting_advice"
                )
            )

        if _has(
            "fertilizer",
            "fertiliser",
            "manure",
            "compost",
            "nutrient",
            "nutrients"
        ):

            topics.append(
                (
                    "Fertilizer Advice",
                    "fertilizer_advice"
                )
            )

        if _has(
            "harvest",
            "harvesting",
            "mature",
            "maturity",
            "ready to harvest"
        ):

            topics.append(
                (
                    "Harvesting Advice",
                    "harvesting_advice"
                )
            )

        return topics

    # ==========================================================
    # BROAD CROP MANAGEMENT / GOOD PRODUCTION
    # ==========================================================

    def _is_broad_crop_management_question():

        broad_phrases = (
            "best farming practices",
            "farming practices",
            "good farming practices",
            "best agricultural practices",
            "crop management",
            "manage my crop",
            "manage the crop",
            "crop care",
            "care for my crop",
            "grow successfully",
            "grow well",
            "good production",
            "better production",
            "improve production",
            "increase production",
            "higher production",
            "successful production",
            "good yield",
            "better yield",
            "increase yield",
            "improve yield",
            "how do i grow",
            "how should i grow",
            "how can i grow",
            "best way to grow",
            "what should i do to grow",
            "how to grow successfully"
        )

        return any(
            phrase in clean_q
            for phrase in broad_phrases
        )

    # ==========================================================
    # UNFAMILIAR / UNKNOWN PEST DETECTION
    # ==========================================================

    def _is_unknown_pest_question():

        unknown_terms = (
            "unfamiliar",
            "unknown",
            "strange",
            "unidentified",
            "new pest",
            "new insect",
            "not sure what pest",
            "not sure what insect",
            "what pest is this",
            "what insect is this",
            "what bug is this",
            "what is this insect",
            "what is this pest",
            "what is this bug",
            "i don't know what pest",
            "i do not know what pest",
            "i don't know what insect",
            "i do not know what insect"
        )

        return any(
            term in clean_q
            for term in unknown_terms
        )

    # ==========================================================
    # UNKNOWN PEST RESPONSE
    # ==========================================================

    def _unknown_pest_response(
        crop_title=None
    ):

        if crop_title:

            return (
                f"🔎 <b>Unidentified Pest on {crop_title}</b><br><br>"

                "If you see an unfamiliar pest, do not immediately apply "
                "a pesticide before identifying the problem.<br><br>"

                "<b>First check:</b><br>"
                "• What part of the plant is being damaged?<br>"
                "• Are there holes, chewing marks, spots, curling or "
                "wilting?<br>"
                "• Can you see the insect, worm, caterpillar or eggs?<br>"
                "• What colour, size and shape is the pest?<br>"
                "• Is the damage spreading quickly?<br>"
                "• Are other plants affected?<br><br>"

                "<b>For a better AgriGuide match, tell me:</b><br>"
                f"1. The crop: {crop_title}<br>"
                "2. What the pest looks like<br>"
                "3. What damage it is causing<br>"
                "4. Which part of the plant is affected<br>"
                "5. When the problem started<br><br>"

                "If possible, provide a clear photo of the pest and "
                "damaged plant for identification by a farmer, extension "
                "worker or agricultural expert.<br><br>"

                "<b>Important:</b> Avoid using an unknown pesticide "
                "without confirming the pest and following the product "
                "label or local agricultural advice."
            )

        return (
            "🔎 <b>Unidentified Pest</b><br><br>"

            "If you see an unfamiliar or unknown pest, AgriGuide needs "
            "more information before matching it to a known pest in the "
            "knowledge base.<br><br>"

            "<b>Please tell me:</b><br>"
            "• Which crop is affected?<br>"
            "• What does the pest look like?<br>"
            "• Is it a worm, caterpillar, fly, beetle, aphid or another "
            "type of insect?<br>"
            "• What damage is it causing?<br>"
            "• Are there holes, spots, yellowing, curling or wilting?<br>"
            "• Which part of the plant is affected?<br>"
            "• Is the problem spreading?<br><br>"

            "If possible, provide a clear photo of the pest and the "
            "damaged plant for identification by an agricultural expert."
            "<br><br>"

            "<b>Important:</b> Do not immediately apply an unknown "
            "pesticide before identifying the pest."
        )

    # ==========================================================
    # SHOW FULL CROP INFORMATION
    # ==========================================================

    def _show_crop_information(
        crop,
        title,
        icon
    ):

        response = (
            f"{icon} <b>{title} Advisory</b><br><br>"
        )

        crop_name = getattr(
            crop,
            "crop_name",
            ""
        )

        category = getattr(
            crop,
            "category",
            ""
        )

        planting_season = getattr(
            crop,
            "planting_season",
            ""
        )

        soil_type = getattr(
            crop,
            "soil_type",
            ""
        )

        planting_advice = getattr(
            crop,
            "planting_advice",
            ""
        )

        fertilizer_advice = getattr(
            crop,
            "fertilizer_advice",
            ""
        )

        pest_info = getattr(
            crop,
            "pest_info",
            ""
        )

        disease_info = getattr(
            crop,
            "disease_info",
            ""
        )

        harvesting_advice = getattr(
            crop,
            "harvesting_advice",
            ""
        )

        if crop_name:

            response += (
                f"<b>Crop:</b> {crop_name}<br>"
            )

        if category:

            response += (
                f"<b>Category:</b> {category}<br>"
            )

        if planting_season:

            response += (
                f"<b>Planting Season:</b> "
                f"{planting_season}<br>"
            )

        if soil_type:

            response += (
                f"<b>Recommended Soil:</b> "
                f"{soil_type}<br>"
            )

        if planting_advice:

            response += (
                f"<b>Planting Advice:</b> "
                f"{planting_advice}<br>"
            )

        if fertilizer_advice:

            response += (
                f"<b>Fertilizer Advice:</b> "
                f"{fertilizer_advice}<br>"
            )

        if pest_info:

            response += (
                f"<b>Pest Information:</b> "
                f"{pest_info}<br>"
            )

        if disease_info:

            response += (
                f"<b>Disease Information:</b> "
                f"{disease_info}<br>"
            )

        if harvesting_advice:

            response += (
                f"<b>Harvesting Advice:</b> "
                f"{harvesting_advice}<br>"
            )

        return response

    # ==========================================================
    # SHOW REQUESTED CROP TOPICS
    # ==========================================================

    def _show_crop_topics(
        crop,
        topics
    ):

        response = ""

        for label, field_name in topics:

            value = getattr(
                crop,
                field_name,
                ""
            )

            if value:

                response += (
                    f"<b>{label}:</b> "
                    f"{value}<br><br>"
                )

        return response

    # ==========================================================
    # SHOW CROP PROBLEMS
    # ==========================================================

    def _show_crop_problems(
        problems,
        title,
        icon,
        focus=None
    ):

        if not problems:

            return (
                f"{icon} <b>{title}</b><br><br>"
                "No matching pest or disease information was found "
                "in the AgriGuide knowledge base."
            )

        response = (
            f"{icon} <b>{title}</b><br><br>"
        )

        if focus is None:

            focus = {
                "all"
            }

        for index, problem in enumerate(
            problems[:10],
            start=1
        ):

            problem_name = getattr(
                problem,
                "problem_name",
                "Unknown problem"
            )

            problem_type = getattr(
                problem,
                "problem_type",
                ""
            )

            symptoms = getattr(
                problem,
                "symptoms",
                ""
            )

            causes = getattr(
                problem,
                "causes",
                ""
            )

            prevention = getattr(
                problem,
                "prevention",
                ""
            )

            control = getattr(
                problem,
                "control_measures",
                ""
            )

            response += (
                f"<b>{index}. {problem_name}</b>"
            )

            if problem_type:

                response += (
                    f" ({problem_type})"
                )

            response += "<br>"

            if (
                "all" in focus
                or "symptoms" in focus
            ):

                if symptoms:

                    response += (
                        f"<b>Symptoms:</b> "
                        f"{symptoms}<br>"
                    )

            if (
                "all" in focus
                or "causes" in focus
            ):

                if causes:

                    response += (
                        f"<b>Causes:</b> "
                        f"{causes}<br>"
                    )

            if (
                "all" in focus
                or "prevention" in focus
            ):

                if prevention:

                    response += (
                        f"<b>Prevention:</b> "
                        f"{prevention}<br>"
                    )

            if (
                "all" in focus
                or "control" in focus
            ):

                if control:

                    response += (
                        f"<b>Control Measures:</b> "
                        f"{control}<br>"
                    )

            response += "<br>"

        return response

    # ==========================================================
    # CROP ANSWER
    # ==========================================================

    def _crop_answer(
        crop_terms,
        crop_title,
        icon
    ):

        crop = _get_crop_advisory(
            crop_terms
        )

        if not crop:

            return (
                f"{icon} <b>{crop_title}</b><br><br>"
                "I could not find detailed crop information for "
                f"{crop_title} in the AgriGuide knowledge base."
            )

        topics = _requested_topics()

        focus = _focuses_from_question()

        wants_disease = _wants_disease()

        wants_pest = _wants_pest()

        # ------------------------------------------------------
        # BROAD FARMING / PRODUCTION QUESTIONS
        #
        # A question such as:
        # "What are the best farming practices for growing sorghum?"
        # or
        # "How should I plant maize for good production?"
        #
        # should return the complete crop advisory rather than
        # only one planting field.
        # ------------------------------------------------------

        if _is_broad_crop_management_question():

            return _show_crop_information(
                crop,
                crop_title,
                icon
            )

        # ------------------------------------------------------
        # If the farmer asks for symptoms/disease/pest
        # information, show the relevant problems.
        # ------------------------------------------------------

        if wants_disease or wants_pest:

            if wants_pest and not wants_disease:

                problems = _get_crop_problems(
                    crop_terms,
                    problem_type="Pest"
                )

                return _show_crop_problems(
                    problems,
                    f"{crop_title} Pests",
                    icon,
                    focus
                )

            if wants_disease and not wants_pest:

                problems = _get_crop_problems(
                    crop_terms,
                    problem_type="Disease"
                )

                return _show_crop_problems(
                    problems,
                    f"{crop_title} Diseases",
                    icon,
                    focus
                )

            problems = _get_crop_problems(
                crop_terms
            )

            return _show_crop_problems(
                problems,
                f"{crop_title} Pests and Diseases",
                icon,
                focus
            )

        # ------------------------------------------------------
        # Requested individual topics
        # ------------------------------------------------------

        if topics:

            topic_response = _show_crop_topics(
                crop,
                topics
            )

            if topic_response:

                return (
                    f"{icon} <b>{crop_title} Advisory</b><br><br>"
                    + topic_response
                )

        # ------------------------------------------------------
        # Otherwise show complete crop information.
        # ------------------------------------------------------

        return _show_crop_information(
            crop,
            crop_title,
            icon
        )

    # ==========================================================
    # CROP CONFIGURATION
    # ==========================================================

    crop_config = [

        (
            "maize",
            ["maize", "corn"],
            ["maize", "corn"],
            "Maize",
            "🌽"
        ),

        (
            "sorghum",
            ["sorghum"],
            ["sorghum"],
            "Sorghum",
            "🌾"
        ),

        (
            "beans",
            ["beans", "common beans"],
            ["beans", "common beans"],
            "Beans",
            "🫘"
        ),

        (
            "groundnuts",
            ["groundnuts", "peanuts"],
            ["groundnuts", "peanuts"],
            "Groundnuts",
            "🥜"
        ),

        (
            "cassava",
            ["cassava"],
            ["cassava"],
            "Cassava",
            "🌱"
        ),

        (
            "rice",
            ["rice"],
            ["rice"],
            "Rice",
            "🌾"
        ),

        (
            "okra",
            ["okra", "ladyfinger"],
            ["okra", "ladyfinger"],
            "Okra",
            "🌿"
        ),

        (
            "sesame",
            ["sesame"],
            ["sesame"],
            "Sesame",
            "🌱"
        ),
    ]

    # ==========================================================
    # PROCESS POST QUESTION
    # ==========================================================

    if request.method == "POST":

        question = request.POST.get(
            "question",
            ""
        ).strip()

        # ------------------------------------------------------
        # LOWERCASE
        # ------------------------------------------------------

        q = question.lower()

        # ------------------------------------------------------
        # REMOVE PUNCTUATION
        # ------------------------------------------------------

        clean_q = re.sub(
            r"[^\w\s]",
            " ",
            q
        )

        # ------------------------------------------------------
        # NORMALIZE SPACES
        # ------------------------------------------------------

        clean_q = re.sub(
            r"\s+",
            " ",
            clean_q
        ).strip()

        words = set(
            clean_q.split()
        )

        # ======================================================
        # INTELLIGENT ALIASES
        # ======================================================

        intelligent_aliases = {

            "crop_health": [
                "crop health",
                "plant health",
                "crop problem",
                "plant problem",
                "crop disease",
                "plant disease",
                "crop is sick",
                "plant is sick",
                "what is wrong with my crop",
                "what is wrong with my plant",
            ],

            "pest_problem": [
                "pest problem",
                "pest attack",
                "pest damage",
                "insect problem",
                "insect attack",
                "insect damage",
                "bug problem",
                "worm problem",
                "caterpillar problem",
            ],

            "prevention": [
                "how can i prevent",
                "how do i prevent",
                "how to prevent",
                "prevent disease",
                "prevent diseases",
                "prevent pests",
                "prevent pest",
                "protect my crop",
                "protect crops",
                "avoid disease",
                "avoid diseases",
                "avoid pests",
            ],

            "control": [
                "how can i control",
                "how do i control",
                "how to control",
                "control disease",
                "control diseases",
                "control pests",
                "control pest",
                "get rid of pests",
                "get rid of pest",
                "treat the disease",
                "treat disease",
            ],

            "planting": [
                "how should i plant",
                "how do i plant",
                "how can i plant",
                "how to plant",
                "how should i grow",
                "how do i grow",
                "how can i grow",
                "how to grow",
                "best way to plant",
                "best way to grow",
            ],

            "fertilizer": [
                "what fertilizer",
                "which fertilizer",
                "how much fertilizer",
                "fertilizer advice",
                "fertiliser advice",
                "use manure",
                "use compost",
            ],

            "harvest": [
                "when should i harvest",
                "when do i harvest",
                "how do i know when to harvest",
                "ready to harvest",
                "harvesting time",
            ],

            "cattle_feeding": [
                "feed cattle",
                "feeding cattle",
                "cattle feeding",
                "feed cow",
                "feeding cow",
                "cow feeding",
                "cattle diet",
                "cow diet",
            ],

            "cattle_sick": [
                "sick cattle",
                "sick cow",
                "cattle is sick",
                "cow is sick",
                "cattle are sick",
                "cows are sick",
                "cattle not eating",
                "cow not eating",
                "cow is not eating",
                "cattle is not eating",
            ],

            "cattle_housing": [
                "cattle housing",
                "cow housing",
                "house cattle",
                "house cows",
                "cattle shelter",
                "cow shelter",
                "cattle shed",
                "cow shed",
                "cattle barn",
            ],

            "cattle_prevention": [
                "prevent cattle disease",
                "prevent cattle diseases",
                "prevent cow disease",
                "prevent cow diseases",
                "protect cattle",
                "protect cows",
                "cattle disease prevention",
                "cow disease prevention",
            ],
        }

        intelligent_matches = {}

        for intent, phrases in intelligent_aliases.items():

            intelligent_matches[intent] = any(
                phrase in clean_q
                for phrase in phrases
            )

        # ======================================================
        # NORMALIZE INTELLIGENT INTENTS
        # ======================================================

        if intelligent_matches["crop_health"]:

            clean_q += " disease symptom"

            words.update(
                (
                    "disease",
                    "symptom"
                )
            )

        if intelligent_matches["pest_problem"]:

            clean_q += " pest insect"

            words.update(
                (
                    "pest",
                    "insect"
                )
            )

        if intelligent_matches["prevention"]:

            clean_q += " prevention prevent"

            words.update(
                (
                    "prevention",
                    "prevent"
                )
            )

        if intelligent_matches["control"]:

            clean_q += " control"

            words.add(
                "control"
            )

        if intelligent_matches["planting"]:

            clean_q += " planting"

            words.add(
                "planting"
            )

        if intelligent_matches["fertilizer"]:

            clean_q += " fertilizer"

            words.add(
                "fertilizer"
            )

        if intelligent_matches["harvest"]:

            clean_q += " harvest"

            words.add(
                "harvest"
            )

        if intelligent_matches["cattle_feeding"]:

            clean_q += " cattle feeding"

            words.update(
                (
                    "cattle",
                    "feeding"
                )
            )

        if intelligent_matches["cattle_sick"]:

            clean_q += " cattle sick"

            words.update(
                (
                    "cattle",
                    "sick"
                )
            )

        if intelligent_matches["cattle_housing"]:

            clean_q += " cattle housing"

            words.update(
                (
                    "cattle",
                    "housing"
                )
            )

        if intelligent_matches["cattle_prevention"]:

            clean_q += " cattle prevention disease"

            words.update(
                (
                    "cattle",
                    "prevention",
                    "disease"
                )
            )

        # ======================================================
        # IDENTIFY MENTIONED CROPS
        # ======================================================

        mentioned_crops = [
            crop
            for crop in crop_config
            if _has(*crop[2])
        ]

        # ======================================================
        # 0A. GREETINGS
        # ======================================================

        greeting_words = {
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "morning",
            "afternoon",
            "evening"
        }

        greeting_phrases = (
            "hello i need some help",
            "hi i need some help",
            "hey i need some help",
            "hello can you help me",
            "hi can you help me",
            "hey can you help me",
            "i need help",
            "i need some help",
            "i need help with farming",
            "help me with farming",
            "can you help me",
            "good morning can you help me",
            "good afternoon can you help me",
            "good evening can you help me"
        )

        if (
            clean_q in greeting_words
            or any(
                phrase in clean_q
                for phrase in greeting_phrases
            )
        ):

            answer = (
                "👋 <b>Welcome to AgriGuide!</b><br><br>"

                "I am your agricultural advisory assistant for "
                "smallholder farmers.<br><br>"

                "<b>You can ask me about:</b><br>"
                "🌽 Maize<br>"
                "🌾 Sorghum<br>"
                "🫘 Beans<br>"
                "🥜 Groundnuts<br>"
                "🌱 Cassava<br>"
                "🌾 Rice<br>"
                "🌿 Okra<br>"
                "🌱 Sesame<br>"
                "🐄 Cattle and livestock<br>"
                "🐛 Pests and diseases<br>"
                "💧 Water conservation<br>"
                "🌱 Farming practices<br>"
                "🌦️ Weather and farming calendar<br><br>"

                "<b>Examples:</b><br>"
                "• How should I plant maize for good production?<br>"
                "• What diseases affect cassava?<br>"
                "• What pest is attacking my maize?<br>"
                "• How can I prevent diseases in cattle?<br>"
                "• What should I feed cattle?<br>"
                "• How can I conserve water on my farm?"
            )

        # ======================================================
        # 0B. THANK YOU
        # ======================================================

        elif _has(
            "thank you",
            "thanks",
            "thank",
            "appreciate"
        ):

            answer = (
                "😊 <b>You are welcome!</b><br><br>"
                "AgriGuide is here to support you with practical "
                "farming information.<br><br>"
                "You can ask another question about crops, pests, "
                "diseases, livestock, water conservation or farming "
                "practices."
            )

        # ======================================================
        # 1. HELP
        # ======================================================

        elif (
            clean_q in (
                "help",
                "help me"
            )
            or _has(
                "what can you do",
                "what can i ask",
                "what questions can i ask",
                "how can you help",
                "what do you know",
                "agri guide",
                "agriguide"
            )
        ):

            answer = (
                "🌱 <b>AgriGuide Assistant Help</b><br><br>"

                "I can provide agricultural advisory information "
                "from the AgriGuide knowledge base.<br><br>"

                "<b>🌽 Crop Advisory</b><br>"
                "Ask about maize, sorghum, beans, groundnuts, "
                "cassava, rice, okra and sesame.<br><br>"

                "<b>🐛 Pest & Disease Identification</b><br>"
                "Describe symptoms such as yellow leaves, holes, "
                "streaks, spots, wilting, curling, rotting or "
                "stunted growth.<br><br>"

                "<b>🌱 Crop Management</b><br>"
                "Ask about soil, planting season, planting methods, "
                "fertilizer, pest management and harvesting.<br><br>"

                "<b>🐄 Livestock</b><br>"
                "Ask about cattle feeding, housing, disease prevention, "
                "management and sick cattle.<br><br>"

                "<b>💧 Water Conservation</b><br>"
                "Ask how to save, manage and conserve water during "
                "dry periods.<br><br>"

                "<b>🌾 Farming Practices</b><br>"
                "Ask about good farming practices and improving crop "
                "production.<br><br>"

                "<b>Example questions:</b><br>"
                "• How should I plant maize for good production?<br>"
                "• What diseases can affect cassava?<br>"
                "• My maize leaves have holes. What pest could be "
                "responsible?<br>"
                "• What should I feed cattle?<br>"
                "• How can I prevent cattle diseases?<br>"
                "• What should I do if I see an unfamiliar pest?"
            )

        # ======================================================
        # 2. SICK CATTLE
        # ======================================================

        elif (
            intelligent_matches["cattle_sick"]
            or (
                _is_cattle()
                and _has(
                    "sick",
                    "ill",
                    "not eating",
                    "weak",
                    "fever",
                    "cough",
                    "diarrhea",
                    "diarrhoea"
                )
            )
        ):

            cattle = _get_cattle_advisory()

            answer = (
                "🐄 <b>Sick Cattle Advisory</b><br><br>"
            )

            if cattle:

                management = getattr(
                    cattle,
                    "management_advice",
                    ""
                )

                feeding = getattr(
                    cattle,
                    "feeding_advice",
                    ""
                )

                housing = getattr(
                    cattle,
                    "housing_advice",
                    ""
                )

                prevention = getattr(
                    cattle,
                    "prevention_advice",
                    ""
                )

                if management:

                    answer += (
                        f"<b>Management:</b> "
                        f"{management}<br><br>"
                    )

                if feeding:

                    answer += (
                        f"<b>Feeding:</b> "
                        f"{feeding}<br><br>"
                    )

                if housing:

                    answer += (
                        f"<b>Housing:</b> "
                        f"{housing}<br><br>"
                    )

                if prevention:

                    answer += (
                        f"<b>Prevention:</b> "
                        f"{prevention}<br><br>"
                    )

            answer += (
                "<b>What to do when a cow is sick:</b><br>"
                "• Separate the sick animal from healthy animals "
                "where practical.<br>"
                "• Provide clean drinking water.<br>"
                "• Provide suitable, clean and easily accessible feed.<br>"
                "• Observe eating, drinking, breathing, movement and "
                "other unusual signs.<br>"
                "• Keep the shelter clean, dry and well ventilated.<br>"
                "• Keep health and treatment records.<br>"
                "• Contact a qualified veterinary professional when "
                "the animal is seriously ill or symptoms persist.<br><br>"

                "<b>Important:</b> Do not give medicines randomly. "
                "Correct treatment depends on the actual disease or "
                "condition.<br><br>"

                "<b>Common cattle health problems include:</b><br>"
                "• Tick-borne diseases<br>"
                "• Foot-and-mouth disease<br>"
                "• Mastitis<br>"
                "• Trypanosomiasis<br>"
                "• Internal and external parasites<br><br>"

                "If you tell me the symptoms you see, I can help "
                "you check the AgriGuide knowledge base for related "
                "advisory information."
            )

        # ======================================================
        # 3. CATTLE FEEDING
        # ======================================================

        elif (
            _is_cattle()
            and _has(
                "feed",
                "feeding",
                "food",
                "diet",
                "eat",
                "eating",
                "nutrition",
                "water"
            )
        ):

            cattle = _get_cattle_advisory()

            answer = (
                "🐄 <b>Cattle Feeding Advisory</b><br><br>"
            )

            if cattle:

                feeding = getattr(
                    cattle,
                    "feeding_advice",
                    ""
                )

                if feeding:

                    answer += (
                        f"{feeding}<br><br>"
                    )

            answer += (
                "<b>Practical feeding guidance:</b><br>"
                "• Provide a balanced diet based on available "
                "pasture and suitable feed resources.<br>"
                "• Provide grasses and other appropriate forage.<br>"
                "• Legumes can help improve the protein content "
                "of the diet when suitable.<br>"
                "• Provide clean drinking water regularly.<br>"
                "• During dry periods, provide conserved feed such "
                "as good-quality hay where available.<br>"
                "• Suitable mineral or nutritional supplements "
                "may be needed depending on the animal's condition "
                "and local advice."
            )

        # ======================================================
        # 4. CATTLE DISEASE PREVENTION
        # ======================================================

        elif (
            _is_cattle()
            and _has(
                "prevent",
                "prevention",
                "protect",
                "avoid"
            )
            and _has(
                "disease",
                "diseases",
                "illness",
                "sick"
            )
        ):

            cattle = _get_cattle_advisory()

            answer = (
                "🐄 <b>Cattle Disease Prevention</b><br><br>"
            )

            if cattle:

                prevention = getattr(
                    cattle,
                    "prevention_advice",
                    ""
                )

                if prevention:

                    answer += (
                        f"<b>AgriGuide Advice:</b> "
                        f"{prevention}<br><br>"
                    )

            answer += (
                "<b>Practical prevention measures:</b><br>"
                "• Keep cattle housing clean and dry.<br>"
                "• Provide clean drinking water.<br>"
                "• Provide adequate and nutritious feed.<br>"
                "• Follow recommended vaccination and disease-control "
                "programmes.<br>"
                "• Isolate visibly sick animals where practical.<br>"
                "• Observe new animals before mixing them with the herd.<br>"
                "• Reduce overcrowding.<br>"
                "• Control ticks and other parasites according to "
                "local veterinary guidance.<br>"
                "• Keep cattle health and treatment records.<br>"
                "• Seek veterinary assistance when serious disease "
                "is suspected."
            )

        # ======================================================
        # 5. CATTLE HOUSING
        # ======================================================

        elif (
            _is_cattle()
            and _has(
                "house",
                "housing",
                "shelter",
                "shed",
                "barn"
            )
        ):

            cattle = _get_cattle_advisory()

            answer = (
                "🐄 <b>Cattle Housing Advisory</b><br><br>"
            )

            if cattle:

                housing = getattr(
                    cattle,
                    "housing_advice",
                    ""
                )

                if housing:

                    answer += (
                        f"<b>AgriGuide Advice:</b> "
                        f"{housing}<br><br>"
                    )

            answer += (
                "<b>Good cattle housing should:</b><br>"
                "• Provide adequate space.<br>"
                "• Protect animals from excessive rain and heat.<br>"
                "• Have good ventilation.<br>"
                "• Remain clean and dry.<br>"
                "• Provide safe access to drinking water.<br>"
                "• Allow easy cleaning and removal of manure.<br>"
                "• Reduce overcrowding and unnecessary contact "
                "between sick and healthy animals."
            )

        # ======================================================
        # 6. GENERAL CATTLE MANAGEMENT
        # ======================================================

        elif (
            _is_cattle()
            and _has(
                "management",
                "manage",
                "care",
                "keep",
                "keeping",
                "maintain"
            )
        ):

            cattle = _get_cattle_advisory()

            answer = (
                "🐄 <b>Cattle Management Advisory</b><br><br>"
            )

            if cattle:

                management = getattr(
                    cattle,
                    "management_advice",
                    ""
                )

                feeding = getattr(
                    cattle,
                    "feeding_advice",
                    ""
                )

                housing = getattr(
                    cattle,
                    "housing_advice",
                    ""
                )

                prevention = getattr(
                    cattle,
                    "prevention_advice",
                    ""
                )

                if management:

                    answer += (
                        f"<b>Management:</b> "
                        f"{management}<br><br>"
                    )

                if feeding:

                    answer += (
                        f"<b>Feeding:</b> "
                        f"{feeding}<br><br>"
                    )

                if housing:

                    answer += (
                        f"<b>Housing:</b> "
                        f"{housing}<br><br>"
                    )

                if prevention:

                    answer += (
                        f"<b>Disease Prevention:</b> "
                        f"{prevention}<br><br>"
                    )

            answer += (
                "Good cattle management combines nutrition, clean "
                "water, suitable housing, disease prevention, "
                "observation and appropriate veterinary support."
            )

        # ======================================================
        # 7. GENERAL CATTLE DISEASES
        # ======================================================

        elif (
            _is_cattle()
            and _has(
                "disease",
                "diseases",
                "illness",
                "symptom",
                "symptoms",
                "health"
            )
        ):

            answer = (
                "🐄 <b>Cattle Health and Diseases</b><br><br>"
                "<b>Common cattle health problems may include:</b><br>"
                "• Tick-borne diseases<br>"
                "• Foot-and-mouth disease<br>"
                "• Mastitis<br>"
                "• Trypanosomiasis<br>"
                "• Internal parasites<br>"
                "• External parasites<br><br>"

                "<b>Prevention:</b><br>"
                "• Good hygiene<br>"
                "• Clean water<br>"
                "• Good nutrition<br>"
                "• Appropriate vaccination and disease-control "
                "programmes<br>"
                "• Isolation of sick animals<br>"
                "• Veterinary assistance when needed<br><br>"

                "If you describe the symptoms of the animal, "
                "AgriGuide can help you identify related information "
                "in its knowledge base."
            )

        # ======================================================
        # 8. FALL ARMYWORM
        # ======================================================

        elif _has(
            "fall armyworm",
            "fall army worm",
            "armyworm",
            "army worm"
        ):

            try:

                problems = PestDisease.objects.filter(
                    Q(problem_name__icontains="fall armyworm")
                    | Q(problem_name__icontains="armyworm")
                ).distinct()

            except Exception:

                problems = PestDisease.objects.none()

            answer = _show_crop_problems(
                problems,
                "Fall Armyworm",
                "🐛",
                _focuses_from_question()
            )

        # ======================================================
        # 9. INTELLIGENT SYMPTOM IDENTIFICATION
        # ======================================================

        elif (
            len(mentioned_crops) == 1
            and _is_symptom_identification_question()
            and not _has(
                "list all diseases",
                "all diseases",
                "what diseases",
                "list diseases",
                "all pests",
                "what pests",
                "list pests"
            )
        ):

            crop_key = mentioned_crops[0]

            answer = _show_symptom_matches(
                crop_key[1],
                crop_key[3],
                crop_key[4]
            )

        # ======================================================
        # 10. MULTIPLE CROPS
        # ======================================================

        elif len(mentioned_crops) >= 2:

            response = (
                "🌱 <b>AgriGuide Multi-Crop Advisory</b><br><br>"
            )

            for crop in mentioned_crops:

                response += _crop_answer(
                    crop[1],
                    crop[3],
                    crop[4]
                )

                response += (
                    "<hr>"
                )

            answer = response

        # ======================================================
        # 11. MAIZE
        # ======================================================

        elif _has(
            "maize",
            "corn"
        ):

            answer = _crop_answer(
                ["maize", "corn"],
                "Maize",
                "🌽"
            )

            # Additional fallback for maize disease questions
            if (
                _wants_disease()
                and not _get_crop_problems(
                    ["maize", "corn"],
                    problem_type="Disease"
                ).exists()
            ):

                answer += (
                    "<br><b>General Maize Disease Guidance:</b><br>"
                    "Use healthy planting material, maintain good field "
                    "hygiene, control weeds, monitor the crop regularly "
                    "and remove or manage affected plants according to "
                    "local agricultural advice."
                )

        # ======================================================
        # 12. SORGHUM
        # ======================================================

        elif _has(
            "sorghum"
        ):

            answer = _crop_answer(
                ["sorghum"],
                "Sorghum",
                "🌾"
            )

        # ======================================================
        # 13. BEANS
        # ======================================================

        elif _has(
            "beans",
            "common beans"
        ):

            answer = _crop_answer(
                ["beans", "common beans"],
                "Beans",
                "🫘"
            )

        # ======================================================
        # 14. GROUNDNUTS
        # ======================================================

        elif _has(
            "groundnuts",
            "peanuts"
        ):

            answer = _crop_answer(
                ["groundnuts", "peanuts"],
                "Groundnuts",
                "🥜"
            )

        # ======================================================
        # 15. CASSAVA
        # ======================================================

        elif _has(
            "cassava"
        ):

            answer = _crop_answer(
                ["cassava"],
                "Cassava",
                "🌱"
            )

            if (
                _wants_disease()
                and not _requested_topics()
            ):

                answer += (
                    "<br><b>Additional Cassava Production Advice:</b><br>"
                    "• Use healthy planting stems.<br>"
                    "• Plant when there is adequate moisture.<br>"
                    "• Prepare the land properly before planting.<br>"
                    "• Control weeds during early crop establishment.<br>"
                    "• Monitor the crop for pests and diseases.<br>"
                    "• Harvest according to the recommended maturity "
                    "period for the variety."
                )

        # ======================================================
        # 16. RICE
        # ======================================================

        elif _has(
            "rice"
        ):

            answer = _crop_answer(
                ["rice"],
                "Rice",
                "🌾"
            )

        # ======================================================
        # 17. OKRA
        # ======================================================

        elif _has(
            "okra",
            "ladyfinger"
        ):

            answer = _crop_answer(
                ["okra", "ladyfinger"],
                "Okra",
                "🌿"
            )

        # ======================================================
        # 18. SESAME
        # ======================================================

        elif _has(
            "sesame"
        ):

            answer = _crop_answer(
                ["sesame"],
                "Sesame",
                "🌱"
            )

        # ======================================================
        # 19. FARMING TIPS
        # ======================================================

        elif _has(
            "farming tips",
            "farm tips",
            "agriculture tips",
            "agricultural tips",
            "farming practices",
            "farm advice",
            "farming advice",
            "general farming",
            "good farming"
        ):

            try:

                tips = (
                    FarmingTip.objects
                    .all()
                    .order_by("-id")[:5]
                )

            except Exception:

                tips = []

            answer = (
                "🌱 <b>AgriGuide Farming Tips</b><br><br>"
            )

            if tips:

                for tip in tips:

                    title = getattr(
                        tip,
                        "title",
                        ""
                    )

                    category = getattr(
                        tip,
                        "category",
                        ""
                    )

                    description = getattr(
                        tip,
                        "description",
                        ""
                    )

                    practical_advice = getattr(
                        tip,
                        "practical_advice",
                        ""
                    )

                    season = getattr(
                        tip,
                        "season",
                        ""
                    )

                    if title:

                        answer += (
                            f"<b>{title}</b><br>"
                        )

                    if category:

                        answer += (
                            f"<b>Category:</b> "
                            f"{category}<br>"
                        )

                    if description:

                        answer += (
                            f"{description}<br>"
                        )

                    if practical_advice:

                        answer += (
                            f"<b>Practical Advice:</b> "
                            f"{practical_advice}<br>"
                        )

                    if season:

                        answer += (
                            f"<b>Season:</b> "
                            f"{season}<br>"
                        )

                    answer += "<br>"

            else:

                answer += (
                    "No farming tips are currently available "
                    "in the knowledge base."
                )

        # ======================================================
        # 20. WATER CONSERVATION
        # ======================================================

        elif _has(
            "water conservation",
            "conserve water",
            "save water",
            "saving water",
            "water management",
            "manage water",
            "water saving",
            "dry period",
            "dry season",
            "lack of water",
            "water shortage"
        ):

            try:

                tips = (
                    FarmingTip.objects
                    .filter(
                        Q(title__icontains="water")
                        | Q(description__icontains="water")
                        | Q(practical_advice__icontains="water")
                    )
                    .distinct()[:5]
                )

            except Exception:

                tips = []

            answer = (
                "💧 <b>Water Conservation on the Farm</b><br><br>"
            )

            if tips:

                for tip in tips:

                    title = getattr(
                        tip,
                        "title",
                        ""
                    )

                    description = getattr(
                        tip,
                        "description",
                        ""
                    )

                    practical_advice = getattr(
                        tip,
                        "practical_advice",
                        ""
                    )

                    if title:

                        answer += (
                            f"<b>{title}</b><br>"
                        )

                    if description:

                        answer += (
                            f"{description}<br>"
                        )

                    if practical_advice:

                        answer += (
                            f"<b>Practical Advice:</b> "
                            f"{practical_advice}<br>"
                        )

                    answer += "<br>"

            answer += (
                "<b>Additional water-saving practices:</b><br>"
                "• Use mulch to reduce evaporation.<br>"
                "• Control weeds because weeds compete for water.<br>"
                "• Improve soil organic matter where possible.<br>"
                "• Reduce runoff and soil erosion.<br>"
                "• Apply irrigation efficiently where irrigation is "
                "available.<br>"
                "• Water crops according to their needs and growth stage.<br>"
                "• Protect water sources from contamination."
            )

        # ======================================================
        # 21. GENERAL LIVESTOCK
        # ======================================================

        elif _has(
            "livestock",
            "animal",
            "animals",
            "cattle",
            "cow",
            "goat",
            "goats",
            "sheep",
            "chicken",
            "chickens",
            "poultry",
            "pig",
            "pigs"
        ):

            try:

                livestock = (
                    LivestockAdvisory.objects
                    .all()
                    .order_by("-id")[:5]
                )

            except Exception:

                livestock = []

            answer = (
                "🐄 <b>AgriGuide Livestock Advisory</b><br><br>"
            )

            if livestock:

                for animal in livestock:

                    animal_name = getattr(
                        animal,
                        "animal_name",
                        ""
                    )

                    category = getattr(
                        animal,
                        "category",
                        ""
                    )

                    management = getattr(
                        animal,
                        "management_advice",
                        ""
                    )

                    feeding = getattr(
                        animal,
                        "feeding_advice",
                        ""
                    )

                    housing = getattr(
                        animal,
                        "housing_advice",
                        ""
                    )

                    prevention = getattr(
                        animal,
                        "prevention_advice",
                        ""
                    )

                    if animal_name:

                        answer += (
                            f"<b>{animal_name}</b><br>"
                        )

                    if category:

                        answer += (
                            f"<b>Category:</b> "
                            f"{category}<br>"
                        )

                    if management:

                        answer += (
                            f"<b>Management:</b> "
                            f"{management}<br>"
                        )

                    if feeding:

                        answer += (
                            f"<b>Feeding:</b> "
                            f"{feeding}<br>"
                        )

                    if housing:

                        answer += (
                            f"<b>Housing:</b> "
                            f"{housing}<br>"
                        )

                    if prevention:

                        answer += (
                            f"<b>Prevention:</b> "
                            f"{prevention}<br>"
                        )

                    answer += "<br>"

            else:

                answer += (
                    "No livestock advisory information is currently "
                    "available."
                )

        # ======================================================
        # 22. UNFAMILIAR / UNKNOWN PEST
        # ======================================================

        elif _is_unknown_pest_question():

            # --------------------------------------------------
            # If the user gives a concrete symptom and exactly
            # one crop is known, allow symptom intelligence to
            # work instead of giving only a generic response.
            # --------------------------------------------------

            detected_symptoms = _detect_symptoms()

            if (
                len(mentioned_crops) == 1
                and detected_symptoms
            ):

                crop_key = mentioned_crops[0]

                answer = _show_symptom_matches(
                    crop_key[1],
                    crop_key[3],
                    crop_key[4]
                )

            elif len(mentioned_crops) == 1:

                crop_key = mentioned_crops[0]

                answer = _unknown_pest_response(
                    crop_key[3]
                )

            else:

                answer = _unknown_pest_response()

        # ======================================================
        # 23. PEST / DISEASE SEARCH WITHOUT CROP
        # ======================================================

        elif (
            _has(
                "pest",
                "pests",
                "disease",
                "diseases",
                "insect",
                "insects",
                "symptom",
                "symptoms"
            )
        ):

            if _wants_pest() and not _wants_disease():

                heading = "Pests"

                problem_type = "Pest"

            elif _wants_disease() and not _wants_pest():

                heading = "Diseases"

                problem_type = "Disease"

            else:

                heading = "Pests and Diseases"

                problem_type = None

            keywords = (
                set(
                    clean_q.split()
                )
                - stop_words
            )

            query = Q()

            for keyword in keywords:

                if len(keyword) < 3:
                    continue

                query |= Q(
                    problem_name__icontains=keyword
                )

                query |= Q(
                    crop_name__icontains=keyword
                )

                query |= Q(
                    symptoms__icontains=keyword
                )

                query |= Q(
                    causes__icontains=keyword
                )

            try:

                problems = PestDisease.objects.filter(
                    query
                )

                if problem_type:

                    problems = problems.filter(
                        problem_type__iexact=problem_type
                    )

                problems = problems.distinct()[:10]

            except Exception:

                problems = PestDisease.objects.none()

            answer = _show_crop_problems(
                problems,
                heading,
                "🐛",
                _focuses_from_question()
            )

        # ======================================================
        # 24. GENERAL CROP SEARCH
        # ======================================================

        elif _has(
            "crop",
            "crops",
            "planting",
            "harvest",
            "fertilizer",
            "fertiliser",
            "soil",
            "season",
            "grow",
            "agriculture",
            "farming"
        ):

            requested_topics = _requested_topics()

            keywords = (
                set(
                    clean_q.split()
                )
                - stop_words
            )

            query = Q()

            for keyword in keywords:

                if len(keyword) < 3:
                    continue

                query |= Q(
                    crop_name__icontains=keyword
                )

                query |= Q(
                    category__icontains=keyword
                )

                query |= Q(
                    planting_season__icontains=keyword
                )

                query |= Q(
                    soil_type__icontains=keyword
                )

                query |= Q(
                    planting_advice__icontains=keyword
                )

                query |= Q(
                    fertilizer_advice__icontains=keyword
                )

                query |= Q(
                    harvesting_advice__icontains=keyword
                )

            try:

                crops = (
                    CropAdvisory.objects
                    .filter(query)
                    .distinct()[:8]
                )

            except Exception:

                crops = []

            if crops:

                response = (
                    "🌱 <b>AgriGuide Crop Information</b><br><br>"
                )

                for crop in crops:

                    crop_name = getattr(
                        crop,
                        "crop_name",
                        "Crop"
                    )

                    if requested_topics:

                        response += (
                            f"<b>{crop_name}</b><br>"
                        )

                        response += _show_crop_topics(
                            crop,
                            requested_topics
                        )

                    else:

                        response += (
                            _show_crop_information(
                                crop,
                                crop_name,
                                "🌱"
                            )
                        )

                    response += "<hr>"

                answer = response

            else:

                answer = (
                    "🌱 <b>AgriGuide Crop Advisory</b><br><br>"
                    "I could not find matching crop information for "
                    "your question.<br><br>"
                    "<b>Available crops include:</b><br>"
                    "Maize, Sorghum, Beans, Groundnuts, Cassava, "
                    "Rice, Okra and Sesame.<br><br>"
                    "You can ask something like:<br>"
                    "• How should I plant maize?<br>"
                    "• What soil is suitable for sorghum?<br>"
                    "• When should I harvest cassava?<br>"
                    "• What fertilizer should I use for maize?"
                )

        # ======================================================
        # 25. GENERIC AGRIGUIDE KNOWLEDGE-BASE SEARCH
        # ======================================================

        else:

            keywords = (
                set(
                    clean_q.split()
                )
                - stop_words
            )

            # --------------------------------------------------
            # Remove very short words
            # --------------------------------------------------

            keywords = {
                word
                for word in keywords
                if len(word) >= 3
            }

            crop_query = Q()

            pest_query = Q()

            tip_query = Q()

            livestock_query = Q()

            for keyword in keywords:

                crop_query |= Q(
                    crop_name__icontains=keyword
                )

                crop_query |= Q(
                    category__icontains=keyword
                )

                crop_query |= Q(
                    planting_season__icontains=keyword
                )

                crop_query |= Q(
                    soil_type__icontains=keyword
                )

                crop_query |= Q(
                    planting_advice__icontains=keyword
                )

                crop_query |= Q(
                    fertilizer_advice__icontains=keyword
                )

                crop_query |= Q(
                    pest_info__icontains=keyword
                )

                crop_query |= Q(
                    disease_info__icontains=keyword
                )

                crop_query |= Q(
                    harvesting_advice__icontains=keyword
                )

                pest_query |= Q(
                    problem_name__icontains=keyword
                )

                pest_query |= Q(
                    crop_name__icontains=keyword
                )

                pest_query |= Q(
                    symptoms__icontains=keyword
                )

                pest_query |= Q(
                    causes__icontains=keyword
                )

                pest_query |= Q(
                    prevention__icontains=keyword
                )

                pest_query |= Q(
                    control_measures__icontains=keyword
                )

                tip_query |= Q(
                    title__icontains=keyword
                )

                tip_query |= Q(
                    category__icontains=keyword
                )

                tip_query |= Q(
                    description__icontains=keyword
                )

                tip_query |= Q(
                    practical_advice__icontains=keyword
                )

                livestock_query |= Q(
                    animal_name__icontains=keyword
                )

                livestock_query |= Q(
                    category__icontains=keyword
                )

                livestock_query |= Q(
                    management_advice__icontains=keyword
                )

                livestock_query |= Q(
                    feeding_advice__icontains=keyword
                )

                livestock_query |= Q(
                    housing_advice__icontains=keyword
                )

                livestock_query |= Q(
                    prevention_advice__icontains=keyword
                )

            try:

                crop_results = (
                    CropAdvisory.objects
                    .filter(crop_query)
                    .distinct()[:3]
                )

            except Exception:

                crop_results = []

            try:

                pest_results = (
                    PestDisease.objects
                    .filter(pest_query)
                    .distinct()[:3]
                )

            except Exception:

                pest_results = []

            try:

                tip_results = (
                    FarmingTip.objects
                    .filter(tip_query)
                    .distinct()[:3]
                )

            except Exception:

                tip_results = []

            try:

                livestock_results = (
                    LivestockAdvisory.objects
                    .filter(livestock_query)
                    .distinct()[:3]
                )

            except Exception:

                livestock_results = []

            response = ""

            # --------------------------------------------------
            # CROP RESULTS
            # --------------------------------------------------

            if crop_results:

                response += (
                    "🌱 <b>Crop Information</b><br><br>"
                )

                for crop in crop_results:

                    crop_name = getattr(
                        crop,
                        "crop_name",
                        "Crop"
                    )

                    response += (
                        f"<b>{crop_name}</b><br>"
                    )

                    planting = getattr(
                        crop,
                        "planting_advice",
                        ""
                    )

                    fertilizer = getattr(
                        crop,
                        "fertilizer_advice",
                        ""
                    )

                    harvest = getattr(
                        crop,
                        "harvesting_advice",
                        ""
                    )

                    if planting:

                        response += (
                            f"<b>Planting:</b> "
                            f"{planting}<br>"
                        )

                    if fertilizer:

                        response += (
                            f"<b>Fertilizer:</b> "
                            f"{fertilizer}<br>"
                        )

                    if harvest:

                        response += (
                            f"<b>Harvest:</b> "
                            f"{harvest}<br>"
                        )

                    response += "<br>"

            # --------------------------------------------------
            # PEST / DISEASE RESULTS
            # --------------------------------------------------

            if pest_results:

                response += (
                    "🐛 <b>Pest and Disease Information</b>"
                    "<br><br>"
                )

                for problem in pest_results:

                    name = getattr(
                        problem,
                        "problem_name",
                        "Problem"
                    )

                    problem_type = getattr(
                        problem,
                        "problem_type",
                        ""
                    )

                    symptoms = getattr(
                        problem,
                        "symptoms",
                        ""
                    )

                    control = getattr(
                        problem,
                        "control_measures",
                        ""
                    )

                    response += (
                        f"<b>{name}</b>"
                    )

                    if problem_type:

                        response += (
                            f" ({problem_type})"
                        )

                    response += "<br>"

                    if symptoms:

                        response += (
                            f"<b>Symptoms:</b> "
                            f"{symptoms}<br>"
                        )

                    if control:

                        response += (
                            f"<b>Control:</b> "
                            f"{control}<br>"
                        )

                    response += "<br>"

            # --------------------------------------------------
            # FARMING TIPS
            # --------------------------------------------------

            if tip_results:

                response += (
                    "🌿 <b>Farming Tips</b><br><br>"
                )

                for tip in tip_results:

                    title = getattr(
                        tip,
                        "title",
                        "Farming Tip"
                    )

                    description = getattr(
                        tip,
                        "description",
                        ""
                    )

                    practical = getattr(
                        tip,
                        "practical_advice",
                        ""
                    )

                    response += (
                        f"<b>{title}</b><br>"
                    )

                    if description:

                        response += (
                            f"{description}<br>"
                        )

                    if practical:

                        response += (
                            f"<b>Practical Advice:</b> "
                            f"{practical}<br>"
                        )

                    response += "<br>"

            # --------------------------------------------------
            # LIVESTOCK RESULTS
            # --------------------------------------------------

            if livestock_results:

                response += (
                    "🐄 <b>Livestock Information</b>"
                    "<br><br>"
                )

                for animal in livestock_results:

                    animal_name = getattr(
                        animal,
                        "animal_name",
                        "Animal"
                    )

                    management = getattr(
                        animal,
                        "management_advice",
                        ""
                    )

                    feeding = getattr(
                        animal,
                        "feeding_advice",
                        ""
                    )

                    response += (
                        f"<b>{animal_name}</b><br>"
                    )

                    if management:

                        response += (
                            f"<b>Management:</b> "
                            f"{management}<br>"
                        )

                    if feeding:

                        response += (
                            f"<b>Feeding:</b> "
                            f"{feeding}<br>"
                        )

                    response += "<br>"

            # --------------------------------------------------
            # FINAL FALLBACK
            # --------------------------------------------------

            if not response:

                response = (
                    "🌱 <b>AgriGuide Assistant</b><br><br>"

                    "I could not find a specific answer to that "
                    "question in the current AgriGuide knowledge base."
                    "<br><br>"

                    "<b>Try asking me about:</b><br>"
                    "• Maize, sorghum, beans, groundnuts, cassava, "
                    "rice, okra or sesame<br>"
                    "• Crop pests and diseases<br>"
                    "• Plant symptoms such as yellowing, spots, holes, "
                    "wilting or curling<br>"
                    "• Cattle feeding and management<br>"
                    "• Cattle diseases and prevention<br>"
                    "• Water conservation<br>"
                    "• Farming practices<br>"
                    "• Planting, fertilizer, soil or harvesting<br><br>"

                    "<b>Example:</b><br>"
                    "\"My maize leaves have holes and are being eaten "
                    "by caterpillars. What should I do?\""
                )

            answer = response

    # ==========================================================
    # EMPTY QUESTION
    # ==========================================================

    if request.method == "POST" and not question:

        answer = (
            "🌱 <b>Please enter a farming question.</b><br><br>"

            "For example:<br>"
            "• How should I plant maize for good production?<br>"
            "• What disease affects cassava?<br>"
            "• My maize leaves have holes. What pest is responsible?<br>"
            "• What should I feed cattle?<br>"
            "• How can I prevent cattle diseases?<br>"
            "• How can I conserve water during a dry period?"
        )

    # ==========================================================
    # RENDER CHATBOT PAGE
    # ==========================================================

    return render(
        request,
        "advisory/chatbot.html",
        {
            "question": question,
            "answer": answer,
        }
    )