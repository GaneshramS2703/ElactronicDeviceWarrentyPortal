from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

 #Home page view that requires user authentication.
@login_required
def home(request):
    """Render the home page."""
    return render(request, 'home.html')
#Health check endpoint for monitoring system status.
def health_check(request):
    return HttpResponse("OK", status=200)
