from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def features_view(request):
    context = {"features_page": "active_page", "features_style":"opacity:1"}
    return render(request, "features.html", context)

def pricing_view(request):
    context = {"price_page": "active_page", "price_style":"opacity:1"}
    return render(request, "pricing.html", context)

def terms_out_view(request):
    return render(request, "terms_out.html", {})

def privacy_out_view(request):
    return render(request, "privacy_out.html", {})