from django.http import HttpResponse
from django.shortcuts import render_to_response

def power_on (request):
    return HttpResponse("12")